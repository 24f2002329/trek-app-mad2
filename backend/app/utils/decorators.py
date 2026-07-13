import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app, g
from app.extensions import db
from app.models.user import User


def generate_token(user):
    payload = {
        "sub": user.id,
        "email": user.email,
        "role": user.role,
        "name": user.name,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        
        payload = decode_token(token)
        if "error" in payload:
            return jsonify({"message": payload["error"]}), 401
            
        user_id = payload.get("sub")
        user = db.session.get(User, user_id)
        if not user or not user.is_active:
            return jsonify({"message": "User not found or inactive"}), 401
            
        g.current_user = user
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(g, "current_user") or g.current_user is None:
                return jsonify({"message": "Authentication required"}), 401
            if g.current_user.role not in roles:
                return jsonify({"message": "Permission denied"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator
