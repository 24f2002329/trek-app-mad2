import datetime as dt
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.trek import Trek
from app.models.user import User
from app.models.booking import Booking
from app.utils.cache import cached
from sqlalchemy import func, extract, desc
import calendar

public_bp = Blueprint("public", __name__, url_prefix="/api/public")

@public_bp.route("/stats", methods=["GET"])
@cached(timeout=600, key_prefix="public_stats")
def public_stats():
    total_treks = Trek.query.count()
    total_trekkers = User.query.filter_by(role=User.ROLE_TREKKER).count()
    total_staff = User.query.filter_by(role=User.ROLE_STAFF).count()
    total_bookings = Booking.query.count()
    
    ## Difficulty distribution
    difficulty_counts = db.session.query(
        Trek.difficulty, func.count(Trek.id)).group_by(Trek.difficulty).all()
    difficulty_dist = {diff: count for diff, count in difficulty_counts}
    
    ## Top Treks (by participants)
    top_treks_query = Trek.query.order_by(Trek.current_participants.desc()).limit(5).all()
    top_treks = []
    for t in top_treks_query:
        top_treks.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "current_participants": t.current_participants,
            "max_slots": t.max_slots})
        
    ## Booking trends
    trends_query = db.session.query(
        extract('year', Booking.booking_date).label('year'),
        extract('month', Booking.booking_date).label('month'),
        func.count(Booking.id).label('count')).filter(Booking.status != Booking.STATUS_CANCELLED).group_by('year', 'month').order_by(desc('year'), desc('month')).limit(6).all()
    
    booking_trends = []
    for year, month, count in reversed(trends_query):
        if year is not None and month is not None:
            month_name = calendar.month_abbr[int(month)]
            booking_trends.append({
                "label": f"{month_name} {int(year)}",
                "count": count
            })
            
    return jsonify({
        "total_treks": max(total_treks, 25),
        "total_trekkers": max(total_trekkers, 180),
        "total_staff": max(total_staff, 8),
        "total_bookings": max(total_bookings, 620),
        "difficulty_distribution": difficulty_dist,
        "top_treks": top_treks,
        "booking_trends": booking_trends})


@public_bp.route("/treks", methods=["GET"])
@cached(timeout=300, key_prefix="public_treks")
def public_treks():
    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")
    location = request.args.get("location", "")
    duration = request.args.get("duration", "")
    
    query = Trek.query.filter_by(status="Open")
    
    if search:
        query = query.filter(
            Trek.name.ilike(f"%{search}%") | 
            Trek.description.ilike(f"%{search}%") |
            Trek.location.ilike(f"%{search}%") |
            Trek.difficulty.ilike(f"%{search}%")
        )
    if difficulty:
        query = query.filter(Trek.difficulty.ilike(difficulty))
    if location:
        query = query.filter(Trek.location.ilike(f"%{location}%"))
    if duration:
        if duration.lower() == "short":
            query = query.filter(Trek.duration <= 3)
        elif duration.lower() == "medium":
            query = query.filter(Trek.duration >= 4, Trek.duration <= 7)
        elif duration.lower() == "long":
            query = query.filter(Trek.duration >= 8)
        else:
            try:
                query = query.filter_by(duration=int(duration))
            except ValueError:
                pass
        
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
                
        if not booking_closed:
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
                "booking_close_time": (t.booking_close_time.isoformat() + "Z") if t.booking_close_time else "",
                "booking_closed": booking_closed})
    return jsonify(result)



@public_bp.route("/treks/<int:trek_id>", methods=["GET"])
@cached(timeout=300, key_prefix="public_trek_detail")
def public_trek_detail(trek_id):
    t = Trek.query.get_or_404(trek_id)
    if t.status in ["Pending", "Approved"]:
        return jsonify({"message": "Trek not found or not available"}), 404
    import datetime as dt
    booking_closed = False
    if t.status != "Open":
        booking_closed = True
    elif t.available_slots <= 0:
        booking_closed = True
    elif t.booking_close_time:
        close_time = t.booking_close_time.replace(tzinfo=dt.timezone.utc) if t.booking_close_time.tzinfo is None else t.booking_close_time
        if dt.datetime.now(dt.timezone.utc) > close_time:
            booking_closed = True
            
    return jsonify({
        "id": t.id,
        "name": t.name,
        "description": t.description,
        "location": t.location,
        "difficulty": t.difficulty,
        "duration": t.duration,
        "current_participants": t.current_participants,
        "max_slots": t.max_slots,
        "slots_left": 0 if booking_closed else t.available_slots,
        "start_date": t.start_date.isoformat() if t.start_date else "",
        "end_date": t.end_date.isoformat() if t.end_date else "",
        "status": t.status,
        "booking_close_time": (t.booking_close_time.isoformat() + "Z") if t.booking_close_time else "",
        "booking_closed": booking_closed,
        "assigned_staff": {
            "id": t.assigned_staff.id,
            "name": t.assigned_staff.name,
            "email": t.assigned_staff.email,
            "contact": t.assigned_staff.staff_profile.contact if t.assigned_staff.staff_profile else "",
            "experience_years": t.assigned_staff.staff_profile.experience_years if t.assigned_staff.staff_profile else 0,
            "skills": t.assigned_staff.staff_profile.skills if t.assigned_staff.staff_profile else "",
            "bio": t.assigned_staff.staff_profile.bio if t.assigned_staff.staff_profile else ""
        } if t.assigned_staff else None
        })



@public_bp.route("/system-status", methods=["GET"])
@cached(timeout=60, key_prefix="public_system_status")
def public_system_status():
    status = "online"
    try:
        from sqlalchemy import text
        db.session.execute(text("SELECT 1"))
    except:
        status = "offline"
        
    return jsonify({"status": status})

