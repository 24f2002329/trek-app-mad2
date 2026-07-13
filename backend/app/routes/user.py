from flask import Blueprint, jsonify, g
from app.models.trek import Trek
from app.models.user import User
from app.models.booking import Booking
from app.utils.decorators import token_required, role_required
import datetime as dt

user_bp = Blueprint("user", __name__, url_prefix="/api/user")

@user_bp.route("/dashboard-summary", methods=["GET"])
@token_required
@role_required(User.ROLE_TREKKER)
def user_dashboard_summary():
    user_id = g.current_user.id
    bookings = Booking.query.filter_by(user_id=user_id).all()
    
    my_bookings = []
    booking_history = []
    upcoming_treks = []
    
    today = dt.date.today()
    
    for b in bookings:
        t = b.trek
        if not t:
            continue
            
        booking_data = {
            "booking_id": b.id,
            "trek_id": t.id,
            "trek_name": t.name,
            "location": t.location,
            "duration": t.duration,
            "start_date": t.start_date.isoformat() if t.start_date else "",
            "booking_date": b.booking_date.isoformat() if b.booking_date else "",
            "slots": b.slots_booked,
            "status": b.status
        }
        
        if b.status == Booking.STATUS_CANCELLED or (t.end_date and t.end_date < today):
            booking_history.append(booking_data)
        else:
            my_bookings.append(booking_data)
            if t.start_date and t.start_date >= today:
                upcoming_treks.append(booking_data)
                
    booked_trek_ids = [b.trek_id for b in bookings]
    recommended_treks = Trek.query.filter(
        Trek.status.in_(["Open", "Approved", "Active"]),
        ~Trek.id.in_(booked_trek_ids) if booked_trek_ids else True
    ).limit(3).all()
    
    recommended_list = []
    for t in recommended_treks:
        recommended_list.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "difficulty": t.difficulty,
            "duration": t.duration,
            "slots_left": t.available_slots
        })
        
    return jsonify({
        "upcoming_treks": upcoming_treks,
        "my_bookings": my_bookings,
        "booking_history": booking_history,
        "recommended_treks": recommended_list
    })
