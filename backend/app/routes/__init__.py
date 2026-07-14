from .public import public_bp
from .admin import admin_bp
from .staff import staff_bp
from .user import user_bp
from .booking import booking_bp
from .auth import auth_bp
from .export import export_bp

def register_blueprints(app):
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(export_bp)