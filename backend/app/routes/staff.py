from flask import Blueprint, jsonify, request, g
from app.extensions import db
from app.models.trek import Trek
from app.models.user import User
from app.models.booking import Booking
from app.models.staff_profile import StaffProfile
from app.utils.decorators import token_required, role_required
import datetime as dt

staff_bp = Blueprint("staff", __name__, url_prefix="/api/staff")

@staff_bp.route("/dashboard-summary", methods=["GET"])
@token_required
@role_required(User.ROLE_STAFF)
def staff_dashboard_summary():
    staff_id = g.current_user.id
    assigned_treks = Trek.query.filter_by(assigned_staff_id=staff_id).all()
    
    today = dt.date.today()
    today_treks = [t for t in assigned_treks if t.start_date <= today <= t.end_date]
    
    treks_list = []
    participants = []
    
    for t in assigned_treks:
        booking_closed = False
        if t.status != "Open":
            booking_closed = True
        elif t.booking_close_time:
            close_time = t.booking_close_time.replace(tzinfo=dt.timezone.utc) if t.booking_close_time.tzinfo is None else t.booking_close_time
            if dt.datetime.now(dt.timezone.utc) > close_time:
                booking_closed = True

        treks_list.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "difficulty": t.difficulty,
            "duration": t.duration,
            "start_date": t.start_date.isoformat() if t.start_date else "",
            "end_date": t.end_date.isoformat() if t.end_date else "",
            "status": t.status,
            "current_participants": t.current_participants,
            "max_slots": t.max_slots,
            "booking_close_time": t.booking_close_time.isoformat() if t.booking_close_time else "",
            "booking_closed": booking_closed
        })
        
        for booking in t.bookings:
            if booking.status != Booking.STATUS_CANCELLED:
                participants.append({
                    "booking_id": booking.id,
                    "trek_id": t.id,
                    "trek_name": t.name,
                    "trekker_name": booking.user.name if booking.user else "Unknown",
                    "email": booking.user.email if booking.user else "",
                    "slots": booking.slots_booked,
                    "status": booking.status,
                    "booking_date": booking.booking_date.isoformat() if booking.booking_date else ""
                })
                
    return jsonify({
        "assigned_treks": treks_list,
        "today_treks": [{
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "status": t.status
        } for t in today_treks],
        "participants": participants
    })

@staff_bp.route("/treks/<int:trek_id>/status", methods=["PUT"])
@token_required
@role_required(User.ROLE_STAFF, User.ROLE_ADMIN)
def update_trek_status(trek_id):
    t = Trek.query.get_or_404(trek_id)
    if g.current_user.role == User.ROLE_STAFF and t.assigned_staff_id != g.current_user.id:
        return jsonify({"message": "Permission denied for this trek"}), 403
        
    data = request.get_json() or {}
    new_status = data.get("status")
    if not new_status:
        return jsonify({"message": "Status is required"}), 400
        
    if new_status not in ["Pending", "Approved", "Open", "Closed", "Completed"]:
        return jsonify({"message": f"Invalid trek status: {new_status}"}), 400
        
    t.status = new_status
    if new_status == "Open":
        t.booking_close_time = None
    elif new_status == "Completed":
        for b in t.bookings:
            if b.status == Booking.STATUS_BOOKED:
                b.status = Booking.STATUS_COMPLETED
                
    db.session.commit()
    return jsonify({"message": "Trek status updated successfully"}), 200

@staff_bp.route("/treks/<int:trek_id>/slots", methods=["PUT"])
@token_required
@role_required(User.ROLE_STAFF)
def update_trek_slots(trek_id):
    t = Trek.query.get_or_404(trek_id)
    if t.assigned_staff_id != g.current_user.id:
        return jsonify({"message": "Permission denied for this trek"}), 403
        
    data = request.get_json() or {}
    max_slots = data.get("max_slots")
    if max_slots is None:
        return jsonify({"message": "max_slots is required"}), 400
        
    try:
        max_slots = int(max_slots)
    except ValueError:
        return jsonify({"message": "Invalid slot number"}), 400
        
    if max_slots < t.current_participants:
        return jsonify({"message": f"Cannot set slots below booked capacity ({t.current_participants})"}), 400
        
    t.max_slots = max_slots
    db.session.commit()
    return jsonify({"message": "Trek slots updated successfully", "max_slots": t.max_slots}), 200

@staff_bp.route("/bookings/<int:booking_id>/status", methods=["PUT"])
@token_required
@role_required(User.ROLE_STAFF)
def update_staff_booking_status(booking_id):
    b = Booking.query.get_or_404(booking_id)
    trek = b.trek
    if not trek:
        return jsonify({"message": "Associated trek not found"}), 404
        
    if trek.assigned_staff_id != g.current_user.id:
        return jsonify({"message": "Permission denied for this trek"}), 403
        
    data = request.get_json() or {}
    new_status = data.get("status")
    if not new_status:
        return jsonify({"message": "Status is required"}), 400
        
    old_status = b.status
    if old_status != new_status:
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
        
    return jsonify({"message": "Booking status updated successfully"}), 200

@staff_bp.route("/profile", methods=["GET"])
@token_required
@role_required(User.ROLE_STAFF)
def get_staff_profile():
    user = g.current_user
    p = user.staff_profile
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "contact": p.contact if p else "",
        "experience_years": p.experience_years if p else 0,
        "skills": p.skills if p else "",
        "bio": p.bio if p else "",
        "is_active": user.is_active
    }), 200

@staff_bp.route("/profile", methods=["PUT"])
@token_required
@role_required(User.ROLE_STAFF)
def update_staff_profile():
    user = g.current_user
    data = request.get_json() or {}
    
    name = data.get("name")
    contact = data.get("contact")
    experience_years = data.get("experience_years")
    skills = data.get("skills")
    bio = data.get("bio")
    
    if name:
        user.name = name
        
    p = user.staff_profile
    if not p:
        p = StaffProfile(user_id=user.id)
        db.session.add(p)
        
    if contact is not None:
        p.contact = contact
    if experience_years is not None:
        try:
            p.experience_years = int(experience_years)
        except ValueError:
            pass
    if skills is not None:
        p.skills = skills
    if bio is not None:
        p.bio = bio
        
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

@staff_bp.route("/treks/<int:trek_id>/close-booking", methods=["PUT"])
@token_required
@role_required(User.ROLE_STAFF, User.ROLE_ADMIN)
def close_trek_booking(trek_id):
    t = Trek.query.get_or_404(trek_id)
    if g.current_user.role == User.ROLE_STAFF and t.assigned_staff_id != g.current_user.id:
        return jsonify({"message": "Permission denied for this trek"}), 403
        
    t.booking_close_time = dt.datetime.now(dt.timezone.utc)
    db.session.commit()
    return jsonify({
        "message": "Booking closed successfully",
        "booking_close_time": t.booking_close_time.isoformat()
    }), 200
