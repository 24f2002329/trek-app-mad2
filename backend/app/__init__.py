from flask import Flask
from flask_cors import CORS

from app.extensions import db
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)               

    from app.routes import register_blueprints
    register_blueprints(app)        

    with app.app_context():
        from app import models  
        db.create_all()

        ## Ensures Admin and Dummy Staff and Trekker exists on app startup
        from app.models.user import User
        from app.models.staff_profile import StaffProfile
        admin_email = "admin@trek.com"
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                name="System Admin",
                email=admin_email,
                role=User.ROLE_ADMIN
            )
            admin.set_password("admin123")
            db.session.add(admin)


            staff_email = "staff@trek.com"
            staff = User.query.filter_by(email=staff_email).first()
            if not staff:
                staff = User(
                    name="John Guide",
                    email=staff_email,
                    role=User.ROLE_STAFF
                )
                staff.set_password("staff123")
                db.session.add(staff)
                db.session.flush()  ##Populate staff.id


                profile = StaffProfile(
                    user_id=staff.id,
                    contact="9876543210",
                    experience_years=5,
                    skills="First Aid, Rock Climbing, Navigation",
                    bio="Experienced guide who loves high-altitude peak climbs."
                )
                db.session.add(profile)


            trekker_email = "trekker@trek.com"
            trekker = User.query.filter_by(email=trekker_email).first()
            if not trekker:
                trekker = User(
                    name="Jane Doe",
                    email=trekker_email,
                    role=User.ROLE_TREKKER
                )
                trekker.set_password("trekker123")
                db.session.add(trekker)

            try:
                db.session.commit()
                print("Default test accounts seeded successfully on app startup.")
            except Exception as e:
                db.session.rollback()
                print(f"Error seeding database on startup: {e}")

    @app.route("/")
    def home():
        return {"message": "API Running"}

    return app
