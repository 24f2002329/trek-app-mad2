from app.extensions import db
from datetime import datetime, timezone


class Booking(db.Model):
    __tablename__ = "bookings"

    STATUS_PENDING = "Pending"
    STATUS_CONFIRMED = "Confirmed"
    STATUS_CANCELLED = "Cancelled"
    STATUS_COMPLETED = "Completed"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)
    booking_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    slots_booked = db.Column(db.Integer, default=1, nullable=False)
    status = db.Column(db.String(20), default=STATUS_PENDING, nullable=False)
    payment_status = db.Column(db.String(20), default="Pending")

    __table_args__ = (db.UniqueConstraint("user_id", "trek_id", name="unique_user_trek_booking"),)

