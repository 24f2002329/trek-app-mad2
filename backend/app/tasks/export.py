import os
from celery import shared_task
from app.models.user import User
from app.models.booking import Booking
from app.services.csv_service import generate_bookings_csv
from app.services.email_service import send_email

@shared_task
def export_user_history_csv(user_id):
    u = User.query.get(user_id)
    if not u:
        return f"Error: User {user_id} not found."
        
    bookings = Booking.query.filter(
        Booking.user_id == user_id,
        Booking.status != Booking.STATUS_CANCELLED).all()
    csv_content = generate_bookings_csv(bookings)
    
    # Establish export path
    export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "exports")
    os.makedirs(export_dir, exist_ok=True)
    
    filename = f"user_{user_id}_history.csv"
    filepath = os.path.join(export_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(csv_content)
        
    # Send email notification
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #121212; color: #e0e0e0; padding: 20px; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #1e1e1e; padding: 30px; border-radius: 12px; border: 1px solid #333;">
            <h2 style="color: #0dcaf0; border-bottom: 1px solid #333; padding-bottom: 10px;">Export Complete! 📊</h2>
            <p>Hi <strong>{u.name}</strong>,</p>
            <p>Your asynchronous export for trekking history has successfully completed.</p>
            <p>You can now download the generated CSV from your bookings page dashboard.</p>
            <p>Thank you for choosing Trekosphere!<br><em>The Trekosphere Team</em></p>
        </div>
    </body>
    </html>
    """
    send_email(u.email, "Trekosphere: Your Trekking History CSV Export is Ready", html_content)
    
    return {
        "status": "Success",
        "filename": filename,
        "records_exported": len(bookings)
    }
