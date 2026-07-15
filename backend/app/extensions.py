from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import redis
import os

db = SQLAlchemy()
mail = Mail()

cache_db = redis.Redis.from_url(os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"))
