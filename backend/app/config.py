import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("SMTP_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("SMTP_PORT", "1025"))
    MAIL_USE_TLS = os.getenv("SMTP_USE_TLS", "false").lower() == "true"
    MAIL_USERNAME = os.getenv("SMTP_USERNAME")
    MAIL_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("SMTP_SENDER", "noreply@treksphere.app")
