from flask import Flask
from flask_cors import CORS

from app.extensions import db, mail
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)               
    mail.init_app(app)

    from app.utils.celery import celery_init_app
    celery_init_app(app)

    from app.routes import register_blueprints
    register_blueprints(app)        

    with app.app_context():
        from app import models  
        db.create_all()

        ## ensure Admin exists on app start
        import os
        from app.models.user import User
        from app.models.staff_profile import StaffProfile
        admin_email = os.getenv("ADMIN_EMAIL", "admin@trek.com")
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                name="System Admin",
                email=admin_email,
                role=User.ROLE_ADMIN
            )
            admin.set_password(os.getenv("ADMIN_PASSWORD", "admin123"))
            db.session.add(admin)
            db.session.commit()

    @app.route("/")
    def home():
        return {"message": "API Running"}

    return app
