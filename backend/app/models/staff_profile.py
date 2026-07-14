from app.extensions import db


class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    contact = db.Column(db.String(20))
    experience_years = db.Column(db.Integer, default=0)
    skills = db.Column(db.String(255))
    bio = db.Column(db.Text)

    user = db.relationship("User", backref=db.backref("staff_profile", uselist=False))
