from app.extensions import db
from datetime import datetime, timezone


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    current_participants = db.Column(db.Integer, default=0, nullable=False)
    max_slots = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    bookings = db.relationship("Booking", backref="trek", lazy=True)
    assigned_staff = db.relationship("User", backref="assigned_treks", foreign_keys=[assigned_staff_id])

    @property
    def available_slots(self):
        return max(0, self.max_slots - self.current_participants)
