import os
from dotenv import load_dotenv
load_dotenv()

from celery.schedules import crontab

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
timezone = "Asia/Kolkata"

imports = (
    "app.tasks.reminder",
    "app.tasks.reports",
    "app.tasks.export",
    "app.tasks.booking_emails",
)

beat_schedule = {
    "send-daily-reminders": {
        "task": "app.tasks.reminder.send_daily_reminders",
        "schedule": crontab(hour=8, minute=0),      ## runs daily at 8:00 AM
    },
    "send-monthly-report": {
        "task": "app.tasks.reports.send_monthly_report",
        "schedule": crontab(day_of_month=1, hour=8, minute=0),      ## runs 1st day of month at 8:00 AM
    },
}
