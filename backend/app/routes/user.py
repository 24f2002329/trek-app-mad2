from flask import Blueprint, request, jsonify, g
from app.extensions import db
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

@user_bp.route("/profile", methods=["GET"])
@token_required
@role_required(User.ROLE_TREKKER)
def get_user_profile():
    user = g.current_user
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_active": user.is_active
    }), 200

@user_bp.route("/profile", methods=["PUT"])
@token_required
@role_required(User.ROLE_TREKKER)
def update_user_profile():
    user = g.current_user
    data = request.get_json() or {}
    
    name = data.get("name")
    password = data.get("password")
    
    if name:
        user.name = name
    if password:
        if len(password) < 8:
            return jsonify({"message": "Password must be at least 8 characters long"}), 400
        user.set_password(password)
        
    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(e)}"}), 500
