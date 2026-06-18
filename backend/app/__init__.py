from flask import Flask

from app.extensions import db
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)                ##Initialize extensions

    from app.routes import bp as routes_bp          ##Register blueprints
    app.register_blueprint(routes_bp)

    with app.app_context():
        from app import models  
        db.create_all()

    @app.route("/")
    def home():
        return {"message": "API Running"}

    return app
