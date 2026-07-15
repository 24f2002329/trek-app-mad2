from flask import Blueprint, jsonify, request, g
from app.extensions import db
from app.models.trek import Trek
from app.models.user import User
from app.models.booking import Booking
from app.models.staff_profile import StaffProfile
from app.utils.decorators import token_required, role_required
from app.utils.cache import cached, invalidate_trek_cache, invalidate_booking_cache
import datetime as dt
import calendar
from sqlalchemy import func, text, extract, desc


admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


# --- Dashboard Summary ---
@admin_bp.route("/dashboard-summary", methods=["GET"])
@token_required
@role_required(User.ROLE_ADMIN)
@cached(timeout=300, key_prefix="admin_summary", user_specific=False)
def admin_dashboard_summary():
    
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role=User.ROLE_TREKKER).count()
    total_bookings = Booking.query.count()
    total_staff = User.query.filter_by(role=User.ROLE_STAFF).count()
    
    
    today = dt.date.today()
    pending_approvals = Trek.query.filter_by(status="Pending").count()
    upcoming_treks = Trek.query.filter(Trek.start_date > today).count()
    treks_starting_today = Trek.query.filter(Trek.start_date == today).count()
    
    cancelled_bookings = Booking.query.filter_by(status=Booking.STATUS_CANCELLED).count()
    
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    recent_list = []
    for b in recent_bookings:
        recent_list.append({
            "id": b.id,
            "trekker_name": b.user.name if b.user else "Unknown",
            "trek_name": b.trek.name if b.trek else "Unknown",
            "slots_booked": b.slots_booked,
            "status": b.status,
            "booking_date": (b.booking_date.isoformat() + "Z") if b.booking_date else ""
        })
        
    return jsonify({
        "total_treks": total_treks,
        "total_users": total_users,
        "total_bookings": total_bookings,
        "total_staff": total_staff,
        "pending_approvals": pending_approvals,
        "upcoming_treks": upcoming_treks,
        "treks_starting_today": treks_starting_today,
        "cancelled_bookings": cancelled_bookings,
        "recent_bookings": recent_list
    })


# --- System Health Status ---
@admin_bp.route("/system-status", methods=["GET"])
@token_required
@role_required(User.ROLE_ADMIN)
def system_status():
    status = {
        "api": "online",
        "database": "offline",
        "redis": "offline",
        "celery": "offline"
    }
    
    ## Test Database
    try:
        db.session.execute(text("SELECT 1"))
        status["database"] = "online"
    except Exception as e:
        status["database"] = f"error: {str(e)}"
        
    ## Test Redis
    try:
        from app.extensions import cache_db
        cache_db.ping()
        status["redis"] = "online"
    except Exception as e:
        status["redis"] = f"error: {str(e)}"
        
    ## test Celery Worker
    try:
        from flask import current_app
        celery = current_app.extensions.get("celery")
        if celery:
            i = celery.control.inspect(timeout=1.0)
            workers = i.ping()
            if workers:
                status["celery"] = "online"
            else:
                status["celery"] = "no workers"
        else:
            status["celery"] = "not initialized"
    except Exception as e:
        status["celery"] = f"error: {str(e)}"
        
    ## Determine overall status
    overall = "online"
    if status["database"] != "online" or status["redis"] != "online" or status["celery"] != "online":
        overall = "degraded"
        
    return jsonify({
        "overall": overall,
        "details": status
    })



# --- Trek Management ---
@admin_bp.route("/treks", methods=["GET"])
@token_required
@role_required(User.ROLE_ADMIN)
def get_all_treks():
    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")
    status = request.args.get("status", "")
    
    query = Trek.query
    
    if search:
        if search.isdigit():
            query = query.filter((Trek.id == int(search)) | Trek.name.ilike(f"%{search}%"))
        else:
            query = query.filter(Trek.name.ilike(f"%{search}%") | Trek.location.ilike(f"%{search}%"))
            
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
        
    if status:
        query = query.filter_by(status=status)
        
    treks = query.all()
    result = []
    for t in treks:
        booking_closed = False
        if t.status != "Open":
            booking_closed = True
        elif t.available_slots <= 0:
            booking_closed = True
        elif t.booking_close_time:
            close_time = t.booking_close_time.replace(tzinfo=dt.timezone.utc) if t.booking_close_time.tzinfo is None else t.booking_close_time
            if dt.datetime.now(dt.timezone.utc) > close_time:
                booking_closed = True

        result.append({
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "location": t.location,
            "difficulty": t.difficulty,
            "duration": t.duration,
            "current_participants": t.current_participants,
            "max_slots": t.max_slots,
            "slots_left": t.available_slots,
            "start_date": t.start_date.isoformat() if t.start_date else "",
            "end_date": t.end_date.isoformat() if t.end_date else "",
            "status": t.status,
            "assigned_staff_id": t.assigned_staff_id,
            "assigned_staff_name": t.assigned_staff.name if t.assigned_staff else "Unassigned",
            "booking_close_time": (t.booking_close_time.isoformat() + "Z") if t.booking_close_time else "",
            "booking_closed": booking_closed
        })
    return jsonify(result)


@admin_bp.route("/treks", methods=["POST"])
@token_required
@role_required(User.ROLE_ADMIN)
def create_trek():
    data = request.get_json() or {}
    name = data.get("name")
    location = data.get("location")
    difficulty = data.get("difficulty")
    max_slots = data.get("max_slots")
    start_date_str = data.get("start_date")
    end_date_str = data.get("end_date")
    
    if not all([name, location, difficulty, max_slots, start_date_str, end_date_str]):
        return jsonify({"message": "Missing required fields"}), 400
        
    try:
        max_slots_int = int(max_slots)
        if max_slots_int <= 0:
            raise ValueError()
    except ValueError:
        return jsonify({"message": "Slots capacity must be a positive integer"}), 400
        
    try:
        start_date = dt.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = dt.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Invalid date format, use YYYY-MM-DD"}), 400
        
    duration = (end_date - start_date).days + 1
    if duration <= 0:
        return jsonify({"message": "End date must be on or after start date"}), 400
        
    booking_close_time_str = data.get("booking_close_time")
    if not booking_close_time_str:
        return jsonify({"message": "Booking close deadline is required"}), 400
        
    try:
        clean_str = booking_close_time_str.split(".")[0].replace("Z", "")
        if "T" in clean_str:
            if len(clean_str.split("T")[1].split(":")) == 2:
                booking_close_time = dt.datetime.strptime(clean_str, "%Y-%m-%dT%H:%M")
            else:
                booking_close_time = dt.datetime.strptime(clean_str, "%Y-%m-%dT%H:%M:%S")
        else:
            booking_close_time = dt.datetime.strptime(clean_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"message": "Invalid booking close deadline format"}), 400
            
    assigned_staff_id = data.get("assigned_staff_id")
    if assigned_staff_id:
        staff_user = User.query.filter_by(id=assigned_staff_id, role=User.ROLE_STAFF).first()
        if not staff_user:
            return jsonify({"message": "Staff member not found or invalid"}), 404
            
    trek = Trek(
        name=name,
        description=data.get("description", ""),
        location=location,
        difficulty=difficulty,
        duration=duration,
        max_slots=int(max_slots),
        start_date=start_date,
        end_date=end_date,
        status=data.get("status", "Pending"),
        assigned_staff_id=assigned_staff_id,
        booking_close_time=booking_close_time
    )
    
    try:
        db.session.add(trek)
        db.session.commit()
        invalidate_trek_cache()
        return jsonify({"message": "Trek created successfully", "id": trek.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500



@admin_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@token_required
@role_required(User.ROLE_ADMIN)
def update_trek(trek_id):
    t = Trek.query.get_or_404(trek_id)
    old_assigned_staff_id = t.assigned_staff_id
    data = request.get_json() or {}
    
    if "name" in data: t.name = data["name"]
    if "description" in data: t.description = data["description"]
    if "location" in data: t.location = data["location"]
    if "difficulty" in data: t.difficulty = data["difficulty"]
    if "max_slots" in data:
        try:
            max_slots_int = int(data["max_slots"])
            if max_slots_int <= 0:
                raise ValueError()
        except ValueError:
            return jsonify({"message": "Slots capacity must be a positive integer"}), 400
        if max_slots_int < t.current_participants:
            return jsonify({"message": f"Cannot set slots below booked capacity ({t.current_participants})"}), 400
        t.max_slots = max_slots_int
    if "status" in data:
        new_status = data["status"]
        if new_status not in ["Pending", "Approved", "Open", "Closed", "Completed", "Active"]:
            return jsonify({"message": f"Invalid trek status: {new_status}"}), 400
        effective_staff_id = data.get("assigned_staff_id", t.assigned_staff_id)
        if new_status == "Approved" and not effective_staff_id:
            return jsonify({"message": "A guide must be assigned before approving this trek."}), 422
        t.status = new_status
        if new_status == "Open":
            t.booking_close_time = None
        elif new_status == "Completed":
            for b in t.bookings:
                if b.status == Booking.STATUS_BOOKED:
                    b.status = Booking.STATUS_COMPLETED
    
    if "start_date" in data:
        try:
            t.start_date = dt.datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"message": "Invalid start_date format, use YYYY-MM-DD"}), 400
            
    if "end_date" in data:
        try:
            t.end_date = dt.datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"message": "Invalid end_date format, use YYYY-MM-DD"}), 400
            

    if t.start_date and t.end_date:
        t.duration = (t.end_date - t.start_date).days + 1
        if t.duration <= 0:
            return jsonify({"message": "End date must be on or after start date"}), 400
            

    if "booking_close_time" in data:
        booking_close_time_str = data["booking_close_time"]
        if not booking_close_time_str:
            return jsonify({"message": "Booking close deadline is required"}), 400
        try:
            clean_str = booking_close_time_str.split(".")[0].replace("Z", "")
            if "T" in clean_str:
                if len(clean_str.split("T")[1].split(":")) == 2:
                    t.booking_close_time = dt.datetime.strptime(clean_str, "%Y-%m-%dT%H:%M")
                else:
                    t.booking_close_time = dt.datetime.strptime(clean_str, "%Y-%m-%dT%H:%M:%S")
            else:
                t.booking_close_time = dt.datetime.strptime(clean_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": "Invalid booking close deadline format"}), 400
                

    if "assigned_staff_id" in data:
        staff_id = data["assigned_staff_id"]
        if staff_id:
            staff_user = User.query.filter_by(id=staff_id, role=User.ROLE_STAFF).first()
            if not staff_user:
                return jsonify({"message": "Staff member not found or invalid"}), 404
            t.assigned_staff_id = staff_id
        else:
            t.assigned_staff_id = None
            
    try:
        db.session.commit()
        invalidate_trek_cache(trek_id=trek_id)
        if old_assigned_staff_id:
            invalidate_booking_cache(guide_id=old_assigned_staff_id)
        if t.assigned_staff_id and t.assigned_staff_id != old_assigned_staff_id:
            invalidate_booking_cache(guide_id=t.assigned_staff_id)
        if t.assigned_staff_id:
            invalidate_booking_cache(guide_id=t.assigned_staff_id)
        for b in t.bookings:
            invalidate_booking_cache(user_id=b.user_id)
        return jsonify({"message": "Trek updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500



@admin_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
@token_required
@role_required(User.ROLE_ADMIN)
def delete_trek(trek_id):
    t = Trek.query.get_or_404(trek_id)
    try:
        booked_user_ids = [b.user_id for b in t.bookings]
        assigned_staff_id = t.assigned_staff_id

        ## cascade delete bookings manually to avoid constraints issues
        Booking.query.filter_by(trek_id=trek_id).delete()
        db.session.delete(t)
        db.session.commit()
        invalidate_trek_cache(trek_id=trek_id)
        if assigned_staff_id:
            invalidate_booking_cache(guide_id=assigned_staff_id)
        for uid in booked_user_ids:
            invalidate_booking_cache(user_id=uid)
        return jsonify({"message": "Trek and associated bookings deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500


# --- Staff Management ---
@admin_bp.route("/staff", methods=["GET"])
@token_required
@role_required(User.ROLE_ADMIN)
def get_all_staff():
    search = request.args.get("search", "")
    query = User.query.filter_by(role=User.ROLE_STAFF)
    
    if search:
        if search.isdigit():
            query = query.filter((User.id == int(search)) | User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))
        else:
            query = query.filter(User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))
            
    staff_members = query.all()
    result = []
    for s in staff_members:
        p = s.staff_profile
        result.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "is_active": s.is_active,
            "contact": p.contact if p else "",
            "experience_years": p.experience_years if p else 0,
            "skills": p.skills if p else "",
            "bio": p.bio if p else ""
        })
    return jsonify(result)


@admin_bp.route("/staff", methods=["POST"])
@token_required
@role_required(User.ROLE_ADMIN)
def create_staff():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    if not all([name, email, password]):
        return jsonify({"message": "Name, email, and password are required"}), 400
        
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User with this email already exists"}), 409
        
    staff_user = User(
        name=name,
        email=email,
        role=User.ROLE_STAFF,
        is_active=True
    )
    staff_user.set_password(password)
    
    try:
        db.session.add(staff_user)
        db.session.flush()
        
        profile = StaffProfile(
            user_id=staff_user.id,
            contact=data.get("contact", ""),
            experience_years=int(data.get("experience_years", 0)),
            skills=data.get("skills", ""),
            bio=data.get("bio", "")
        )
        db.session.add(profile)
        db.session.commit()
        return jsonify({"message": "Staff member created successfully", "id": staff_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500



@admin_bp.route("/staff/<int:staff_id>", methods=["PUT"])
@token_required
@role_required(User.ROLE_ADMIN)
def update_staff(staff_id):
    staff_user = User.query.filter_by(id=staff_id, role=User.ROLE_STAFF).first_or_404()
    data = request.get_json() or {}
    
    if "name" in data: staff_user.name = data["name"]
    if "email" in data:
        existing = User.query.filter_by(email=data["email"]).first()
        if existing and existing.id != staff_id:
            return jsonify({"message": "Email already in use"}), 409
        staff_user.email = data["email"]
        
    if "is_active" in data:
        staff_user.is_active = bool(data["is_active"])
        
    p = staff_user.staff_profile
    if not p:
        p = StaffProfile(user_id=staff_user.id)
        db.session.add(p)
        
    if "contact" in data: p.contact = data["contact"]
    if "experience_years" in data: p.experience_years = int(data["experience_years"])
    if "skills" in data: p.skills = data["skills"]
    if "bio" in data: p.bio = data["bio"]
    
    try:
        db.session.commit()
        return jsonify({"message": "Staff member updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500


@admin_bp.route("/staff/<int:staff_id>/status", methods=["PUT"])
@token_required
@role_required(User.ROLE_ADMIN)
def toggle_staff_status(staff_id):
    staff_user = User.query.filter_by(id=staff_id, role=User.ROLE_STAFF).first_or_404()
    data = request.get_json() or {}
    is_active = data.get("is_active")
    
    if is_active is None:
        return jsonify({"message": "is_active field is required"}), 400
        
    staff_user.is_active = bool(is_active)
    db.session.commit()
    return jsonify({"message": f"Staff status updated to {'Active' if staff_user.is_active else 'Deactivated'}"}), 200


# --- User/Trekker Management ---
@admin_bp.route("/users", methods=["GET"])
@token_required
@role_required(User.ROLE_ADMIN)
def get_all_users():
    search = request.args.get("search", "")
    query = User.query.filter_by(role=User.ROLE_TREKKER)
    
    if search:
        if search.isdigit():
            query = query.filter((User.id == int(search)) | User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))
        else:
            query = query.filter(User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))
            
    users = query.all()
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "is_active": u.is_active,
            "created_at": (u.created_at.isoformat() + "Z") if u.created_at else "",
            "bookings_count": len(u.bookings)
        })
    return jsonify(result)


@admin_bp.route("/users/<int:user_id>/status", methods=["PUT"])
@token_required
@role_required(User.ROLE_ADMIN)
def toggle_user_status(user_id):
    user = User.query.filter_by(id=user_id, role=User.ROLE_TREKKER).first_or_404()
    data = request.get_json() or {}
    is_active = data.get("is_active")
    
    if is_active is None:
        return jsonify({"message": "is_active field is required"}), 400
        
    user.is_active = bool(is_active)
    db.session.commit()
    return jsonify({"message": f"User status updated to {'Active' if user.is_active else 'Deactivated'}"}), 200



@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@token_required
@role_required(User.ROLE_ADMIN)
def get_user_detail(user_id):
    u = User.query.filter_by(id=user_id, role=User.ROLE_TREKKER).first_or_404()
    bookings = []
    for b in u.bookings:
        t = b.trek
        bookings.append({
            "booking_id": b.id,
            "trek_name": t.name if t else "Unknown",
            "location": t.location if t else "",
            "start_date": t.start_date.isoformat() if t and t.start_date else "",
            "status": b.status,
            "payment_status": b.payment_status,
            "slots_booked": b.slots_booked,
            "booking_date": (b.booking_date.isoformat() + "Z") if b.booking_date else ""
        })
    return jsonify({
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "phone": u.phone or "",
        "blood_group": u.blood_group or "",
        "medical_conditions": u.medical_conditions or "",
        "emergency_contact_name": u.emergency_contact_name or "",
        "emergency_contact_phone": u.emergency_contact_phone or "",
        "is_active": u.is_active,
        "created_at": (u.created_at.isoformat() + "Z") if u.created_at else "",
        "bookings_count": len(u.bookings),
        "bookings": bookings
    }), 200



@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
@token_required
@role_required(User.ROLE_ADMIN)
def update_user_detail(user_id):
    u = User.query.filter_by(id=user_id, role=User.ROLE_TREKKER).first_or_404()
    data = request.get_json() or {}

    if "name" in data and data["name"].strip():
        u.name = data["name"].strip()
    if "phone" in data:
        u.phone = data["phone"].strip() or None
    if "blood_group" in data:
        u.blood_group = data["blood_group"].strip() or None
    if "medical_conditions" in data:
        u.medical_conditions = data["medical_conditions"].strip() or None
    if "emergency_contact_name" in data:
        u.emergency_contact_name = data["emergency_contact_name"].strip() or None
    if "emergency_contact_phone" in data:
        u.emergency_contact_phone = data["emergency_contact_phone"].strip() or None

    try:
        db.session.commit()
        return jsonify({"message": "Trekker details updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating user: {str(e)}"}), 500



# --- Booking Management ---
@admin_bp.route("/bookings", methods=["GET"])
@token_required
@role_required(User.ROLE_ADMIN)
def get_all_bookings():
    search = request.args.get("search", "")
    status = request.args.get("status", "")
    
    query = Booking.query
    
    if status:
        query = query.filter_by(status=status)
        
    bookings = query.all()
    result = []
    for b in bookings:
        if search:
            match = False
            if b.user and search.lower() in b.user.name.lower():
                match = True
            if b.trek and search.lower() in b.trek.name.lower():
                match = True
            if not match:
                continue
                
        result.append({
            "id": b.id,
            "user_id": b.user_id,
            "user_name": b.user.name if b.user else "Unknown",
            "user_email": b.user.email if b.user else "",
            "trek_id": b.trek_id,
            "trek_name": b.trek.name if b.trek else "Unknown",
            "trek_location": b.trek.location if b.trek else "",
            "slots_booked": b.slots_booked,
            "status": b.status,
            "payment_status": b.payment_status,
            "booking_date": (b.booking_date.isoformat() + "Z") if b.booking_date else ""
        })
    return jsonify(result)



@admin_bp.route("/bookings/<int:booking_id>/status", methods=["PUT"])
@token_required
@role_required(User.ROLE_ADMIN)
def update_booking_status(booking_id):
    b = Booking.query.get_or_404(booking_id)
    data = request.get_json() or {}
    new_status = data.get("status")
    
    if not new_status:
        return jsonify({"message": "Status is required"}), 400
        
    old_status = b.status
    if old_status != new_status:
        trek = b.trek
        if not trek:
            return jsonify({"message": "Associated trek not found"}), 404
            
        if new_status == Booking.STATUS_CANCELLED:
             if old_status != Booking.STATUS_CANCELLED:
                trek.current_participants = max(0, trek.current_participants - b.slots_booked)
        else:
            if old_status == Booking.STATUS_CANCELLED:
                if trek.available_slots < b.slots_booked:
                    return jsonify({"message": f"Cannot change status: only {trek.available_slots} slots left on trek"}), 400
                trek.current_participants += b.slots_booked
                
        b.status = new_status
        db.session.commit()
        invalidate_trek_cache(trek_id=trek.id)
        invalidate_booking_cache(user_id=b.user_id, guide_id=trek.assigned_staff_id)
        
        # Trigger email alerts on status changes
        if new_status == Booking.STATUS_CANCELLED:
            from app.tasks.booking_emails import send_booking_cancellation_email
            send_booking_cancellation_email.delay(b.user.email, b.user.name, trek.name)
        elif new_status == Booking.STATUS_BOOKED:
            from app.tasks.booking_emails import send_booking_confirmation_email
            send_booking_confirmation_email.delay(b.id)
            
    return jsonify({"message": "Booking status updated successfully"}), 200



# --- Stats and reports ---
@admin_bp.route("/reports/stats", methods=["GET"])
@token_required
@role_required(User.ROLE_ADMIN)
def get_reports_stats():
    difficulty_counts = db.session.query(
        Trek.difficulty, func.count(Trek.id)
    ).group_by(Trek.difficulty).all()
    difficulty_dist = {diff: count for diff, count in difficulty_counts}
    

    status_counts = db.session.query(
        Trek.status, func.count(Trek.id)
    ).group_by(Trek.status).all()
    status_dist = {status: count for status, count in status_counts}
    

    booking_status_counts = db.session.query(
        Booking.status, func.count(Booking.id)
    ).group_by(Booking.status).all()
    booking_status_dist = {status: count for status, count in booking_status_counts}
    

    top_treks_query = Trek.query.order_by(Trek.current_participants.desc()).limit(5).all()
    top_treks = []
    for t in top_treks_query:
        top_treks.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "current_participants": t.current_participants,
            "max_slots": t.max_slots
        })
        

    total_slots_booked = db.session.query(func.sum(Booking.slots_booked)).filter(Booking.status != Booking.STATUS_CANCELLED).scalar() or 0
    total_bookings = Booking.query.count()
    total_users = User.query.filter_by(role=User.ROLE_TREKKER).count()
    total_staff = User.query.filter_by(role=User.ROLE_STAFF).count()
    

    trends_query = db.session.query(
        extract('year', Booking.booking_date).label('year'),
        extract('month', Booking.booking_date).label('month'),
        func.count(Booking.id).label('count')
    ).filter(Booking.status != Booking.STATUS_CANCELLED).group_by('year', 'month').order_by(desc('year'), desc('month')).limit(6).all()
    
    booking_trends = []
    for year, month, count in reversed(trends_query):
        if year is not None and month is not None:
            month_name = calendar.month_abbr[int(month)]
            booking_trends.append({
                "label": f"{month_name} {int(year)}",
                "count": count
            })
            
    return jsonify({
        "difficulty_distribution": difficulty_dist,
        "trek_status_distribution": status_dist,
        "booking_status_distribution": booking_status_dist,
        "top_treks": top_treks,
        "booking_trends": booking_trends,
        "metrics": {
            "total_slots_booked": int(total_slots_booked),
            "total_bookings": total_bookings,
            "total_users": total_users,
            "total_staff": total_staff
        }
    })
