from flask import Blueprint, jsonify, request, g
from app.extensions import db
from app.models.trek import Trek
from app.models.user import User
from app.models.booking import Booking
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
            "max_slots": t.max_slots
        })
        
        for booking in t.bookings:
            if booking.status != Booking.STATUS_CANCELLED:
                participants.append({
                    "trek_name": t.name,
                    "trekker_name": booking.user.name if booking.user else "Unknown",
                    "email": booking.user.email if booking.user else "",
                    "slots": booking.slots_booked,
                    "status": booking.status
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
        
    t.status = new_status
    db.session.commit()
    return jsonify({"message": "Trek status updated successfully"}), 200
