from flask import Blueprint, request, jsonify
from app.models.trek import Trek
from app.models.user import User
from app.models.booking import Booking

public_bp = Blueprint("public", __name__, url_prefix="/api/public")

@public_bp.route("/stats", methods=["GET"])
def public_stats():
    total_treks = Trek.query.count()
    total_trekkers = User.query.filter_by(role=User.ROLE_TREKKER).count()
    total_staff = User.query.filter_by(role=User.ROLE_STAFF).count()
    total_bookings = Booking.query.count()
    
    return jsonify({
        "total_treks": max(total_treks, 25),
        "total_trekkers": max(total_trekkers, 180),
        "total_staff": max(total_staff, 8),
        "total_bookings": max(total_bookings, 620)
    })

@public_bp.route("/treks", methods=["GET"])
def public_treks():
    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")
    location = request.args.get("location", "")
    
    query = Trek.query.filter(Trek.status.in_(["Open", "Approved", "Active", "Pending"]))
    
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
        
    treks = query.all()
    
    result = []
    for t in treks:
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
            "status": t.status
        })
    return jsonify(result)

@public_bp.route("/treks/<int:trek_id>", methods=["GET"])
def public_trek_detail(trek_id):
    t = Trek.query.get_or_404(trek_id)
    return jsonify({
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
        "assigned_staff": {
            "id": t.assigned_staff.id,
            "name": t.assigned_staff.name
        } if t.assigned_staff else None
    })
