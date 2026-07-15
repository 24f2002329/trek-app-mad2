import os
from celery import shared_task
from flask import render_template
from app.services.report_service import get_monthly_report_data
from app.services.email_service import send_email
from app.models.user import User

@shared_task
def send_monthly_report():
    data = get_monthly_report_data()

    html_content = render_template("monthly_report.html", data=data)
    
    admin_email_env = os.getenv("ADMIN_EMAIL")
    if admin_email_env:
        admin_emails = [email.strip() for email in admin_email_env.split(",") if email.strip()]
    else:
        admin_users = User.query.filter_by(role=User.ROLE_ADMIN).all()
        admin_emails = [u.email for u in admin_users]
        if not admin_emails:
            admin_emails = ["admin@trek.com"]
        
    for email in admin_emails:
        send_email(email, f"TrekSphere: Monthly Trekking Activity Report ({data['month_name']})", html_content)
        
    return f"Monthly report task completed. Rendered and sent to {len(admin_emails)} admin(s)."
