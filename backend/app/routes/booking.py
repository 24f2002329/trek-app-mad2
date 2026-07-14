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
    slots = 1  # Force single-slot booking
    
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
    if existing and existing.status != Booking.STATUS_CANCELLED:
        return jsonify({"message": "You have already booked this trek"}), 400
        
    # Check for date overlaps with other active bookings
    active_bookings = Booking.query.filter(
        Booking.user_id == user_id,
        Booking.status.in_([Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED]),
        Booking.trek_id != trek_id
    ).all()
    for ab in active_bookings:
        et = ab.trek
        if et and et.start_date and et.end_date and trek.start_date and trek.end_date:
            if et.start_date <= trek.end_date and et.end_date >= trek.start_date:
                start_str = et.start_date.strftime('%d-%b-%Y')
                end_str = et.end_date.strftime('%d-%b-%Y')
                return jsonify({
                    "message": f"You can't book this slot as you already have a booking for these dates (Trek: {et.name} from {start_str} to {end_str})"
                }), 400
                
    if existing:  # must be STATUS_CANCELLED
        existing.status = Booking.STATUS_PENDING
        existing.slots_booked = slots
        trek.current_participants += slots
        try:
            db.session.commit()
            return jsonify({"message": "Booking request submitted successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error reactivating booking: {str(e)}"}), 500
            
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

@booking_bp.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
@token_required
@role_required(User.ROLE_TREKKER)
def cancel_booking(booking_id):
    user_id = g.current_user.id
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first_or_404()
    
    if booking.status == Booking.STATUS_CANCELLED:
        return jsonify({"message": "Booking is already cancelled"}), 400
        
    trek = booking.trek
    if not trek:
        return jsonify({"message": "Associated trek not found"}), 404
        
    import datetime as dt
    today = dt.date.today()
    if trek.start_date and trek.start_date <= today:
        return jsonify({"message": "Cannot cancel a booking for a trek that has already started"}), 400
        
    old_status = booking.status
    booking.status = Booking.STATUS_CANCELLED
    
    if old_status in [Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED]:
        trek.current_participants = max(0, trek.current_participants - booking.slots_booked)
        
    try:
        db.session.commit()
        return jsonify({"message": "Booking cancelled successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error cancelling booking: {str(e)}"}), 500
