import re
from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.user import User
from app.utils.decorators import generate_token, token_required, role_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "Name, email, and password are required"}), 400

    if len(name.strip()) < 3:
        return jsonify({"message": "Name must be at least 3 characters long"}), 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Invalid email address format"}), 400
    if len(password) < 8:
        return jsonify({"message": "Password must be at least 8 characters long"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User with this email already exists"}), 409

    ## registration is only for Trekkers/users
    user = User(
        name=name,
        email=email,
        role=User.ROLE_TREKKER
    )
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error registering user: {str(e)}"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Invalid email address format"}), 400
    if len(password) < 8:
        return jsonify({"message": "Password must be at least 8 characters long"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"message": "Account has been deactivated"}), 403

    token = generate_token(user)
    
    
    redirect_target = "/user/dashboard"
    if user.is_admin:
        redirect_target = "/admin/dashboard"
    elif user.is_staff:
        redirect_target = "/staff/dashboard"

    return jsonify({
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        },
        "redirect": redirect_target
    }), 200


@auth_bp.route("/me", methods=["GET"])
@token_required
def get_me():
    user = g.current_user
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200
