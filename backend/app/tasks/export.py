import os
from celery import shared_task
from app.models.user import User
from app.models.booking import Booking
from app.services.csv_service import generate_bookings_csv
from app.services.email_service import send_email, render_email_template
import datetime as dt


@shared_task
def export_user_history_csv(user_id):
    u = User.query.get(user_id)
    if not u:
        return f"Error: User {user_id} not found."
        
    today = dt.date.today()
    bookings = Booking.query.filter(Booking.user_id == user_id).all()
    history_bookings = []
    
    for b in bookings:
        t = b.trek
        if not t:
            continue
        if b.status in [Booking.STATUS_CANCELLED, Booking.STATUS_COMPLETED] or (t.end_date and t.end_date < today) or t.status == "Completed":
            history_bookings.append(b)
            
    csv_content = generate_bookings_csv(history_bookings)
    

    export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "exports")
    os.makedirs(export_dir, exist_ok=True)
    
    filename = f"user_{user_id}_history.csv"
    filepath = os.path.join(export_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(csv_content)


    body_html = f"""
    <h2 style="color: #0891b2; margin-top: 0; margin-bottom: 16px; font-size: 20px; font-weight: 700; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">Export Complete! 📊</h2>
    <p style="color: #fff; margin: 0 0 12px 0;">Hi <strong style="color: #0f172a;">{u.name}</strong>,</p>
    <p style="color: #fff; margin: 0 0 12px 0;">Your asynchronous export for trekking history has successfully completed.</p>
    <p style="color: #fff; margin: 0 0 12px 0;">You can now download the generated CSV from your trek history page.</p>
    """
    html_content = render_email_template("Export Complete", body_html)
    send_email(u.email, "TrekSphere: Your Trekking History CSV Export is Ready", html_content)
    
    return {
        "status": "Success",
        "filename": filename,
        "records_exported": len(history_bookings)
    }



@shared_task
def export_user_bookings_csv(user_id):
    u = User.query.get(user_id)
    if not u:
        return f"Error: User {user_id} not found."
        
    today = dt.date.today()
    bookings = Booking.query.filter(Booking.user_id == user_id).all()
    active_bookings = []
    
    for b in bookings:
        t = b.trek
        if not t:
            continue
        is_history = b.status in [Booking.STATUS_CANCELLED, Booking.STATUS_COMPLETED] or (t.end_date and t.end_date < today) or t.status == "Completed"
        if not is_history and b.status == Booking.STATUS_BOOKED:
            active_bookings.append(b)
            
    csv_content = generate_bookings_csv(active_bookings)
    

    export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "exports")
    os.makedirs(export_dir, exist_ok=True)
    
    filename = f"user_{user_id}_bookings.csv"
    filepath = os.path.join(export_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(csv_content)


    body_html = f"""
    <h2 style="color: #0891b2; margin-top: 0; margin-bottom: 16px; font-size: 20px; font-weight: 700; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">Export Complete! 📊</h2>
    <p style="color: #fff; margin: 0 0 12px 0;">Hi <strong style="color: #0f172a;">{u.name}</strong>,</p>
    <p style="color: #fff; margin: 0 0 12px 0;">Your asynchronous export for active bookings has successfully completed.</p>
    <p style="color: #fff; margin: 0 0 12px 0;">You can now download the generated CSV from your bookings page.</p>
    """
    html_content = render_email_template("Export Complete", body_html)
    send_email(u.email, "TrekSphere: Your Active Bookings CSV Export is Ready", html_content)
    
    return {
        "status": "Success",
        "filename": filename,
        "records_exported": len(active_bookings)
    }
