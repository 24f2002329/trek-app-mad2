from flask_sqlalchemy import SQLAlchemy
import redis
import os

db = SQLAlchemy()

cache_db = redis.Redis.from_url(os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"))
