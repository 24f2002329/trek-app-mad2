import os
from app import create_app, db
from app.models import User

def pre_create_admin():
    app = create_app()
    with app.app_context():
        admin_email = "admin@trek.com"
        admin_name = "System Admin"
        admin_password = "admin123"

        existing_admin = User.query.filter_by(email=admin_email).first()
        if existing_admin:
            print(f"Admin user '{admin_email}' already exists.")
            return

        admin = User(
            name=admin_name,
            email=admin_email,
            role=User.ROLE_ADMIN
        )
        admin.set_password(admin_password)

        try:
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user '{admin_email}' pre-created successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {e}")

if __name__ == "__main__":
    pre_create_admin()
