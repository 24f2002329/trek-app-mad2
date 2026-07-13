from flask import Blueprint, jsonify
from app.models.trek import Trek
from app.models.user import User
from app.models.booking import Booking
from app.utils.decorators import token_required, role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.route("/dashboard-summary", methods=["GET"])
@token_required
@role_required(User.ROLE_ADMIN)
def admin_dashboard_summary():
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role=User.ROLE_TREKKER).count()
    total_bookings = Booking.query.count()
    total_staff = User.query.filter_by(role=User.ROLE_STAFF).count()
    
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    recent_list = []
    for b in recent_bookings:
        recent_list.append({
            "id": b.id,
            "trekker_name": b.user.name if b.user else "Unknown",
            "trek_name": b.trek.name if b.trek else "Unknown",
            "slots_booked": b.slots_booked,
            "status": b.status,
            "booking_date": b.booking_date.isoformat() if b.booking_date else ""
        })
        
    return jsonify({
        "total_treks": total_treks,
        "total_users": total_users,
        "total_bookings": total_bookings,
        "total_staff": total_staff,
        "recent_bookings": recent_list
    })
