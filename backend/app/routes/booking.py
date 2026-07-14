from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.trek import Trek
from app.models.user import User
from app.models.booking import Booking
from app.utils.decorators import token_required, role_required

booking_bp = Blueprint("booking", __name__, url_prefix="/api/booking")

@booking_bp.route("/bookings", methods=["POST"])
@token_required
@role_required(User.ROLE_TREKKER)
def create_booking():
    user_id = g.current_user.id
    data = request.get_json() or {}
    trek_id = data.get("trek_id")
    slots = data.get("slots", 1)
    
    if not trek_id:
        return jsonify({"message": "Trek ID is required"}), 400
        
    trek = Trek.query.get_or_404(trek_id)
    if trek.status not in ["Open", "Approved"]:
        return jsonify({"message": "Trek is not open for bookings"}), 400
        
    import datetime as dt
    if trek.booking_close_time:
        close_time = trek.booking_close_time.replace(tzinfo=dt.timezone.utc) if trek.booking_close_time.tzinfo is None else trek.booking_close_time
        if dt.datetime.now(dt.timezone.utc) > close_time:
            return jsonify({"message": "Booking window for this trek has closed"}), 400
        
    if trek.available_slots < slots:
        return jsonify({"message": f"Only {trek.available_slots} slots left"}), 400
        
    existing = Booking.query.filter_by(user_id=user_id, trek_id=trek_id).first()
    if existing:
        if existing.status == Booking.STATUS_CANCELLED:
            existing.status = Booking.STATUS_PENDING
            existing.slots_booked = slots
            trek.current_participants += slots
            db.session.commit()
            return jsonify({"message": "Booking request submitted successfully"}), 201
        return jsonify({"message": "You have already booked this trek"}), 400
        
    booking = Booking(
        user_id=user_id,
        trek_id=trek_id,
        slots_booked=slots,
        status=Booking.STATUS_PENDING
    )
    trek.current_participants += slots
    
    try:
        db.session.add(booking)
        db.session.commit()
        return jsonify({"message": "Booking request submitted successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error booking trek: {str(e)}"}), 500
