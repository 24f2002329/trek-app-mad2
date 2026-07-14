import datetime
from celery import shared_task
from app.models.trek import Trek
from app.models.booking import Booking
from app.services.email_service import send_email

@shared_task
def send_daily_reminders():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    
    # Find treks starting tomorrow
    treks = Trek.query.filter_by(start_date=tomorrow).filter(Trek.status.in_(["Approved", "Open", "Closed"])).all()
    
    count = 0
    for t in treks:
        # Get active bookings
        bookings = Booking.query.filter_by(trek_id=t.id, status=Booking.STATUS_BOOKED).all()
        for b in bookings:
            if not b.user:
                continue
            
            user_name = b.user.name
            to_email = b.user.email
            
            # HTML email template
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #121212; color: #e0e0e0; padding: 20px; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #1e1e1e; padding: 30px; border-radius: 12px; border: 1px solid #333;">
                    <h2 style="color: #0dcaf0; border-bottom: 1px solid #333; padding-bottom: 10px;">Upcoming Trek Reminder! 🏔️</h2>
                    <p>Hi <strong>{user_name}</strong>,</p>
                    <p>This is a friendly reminder that your upcoming adventure is starting tomorrow!</p>
                    
                    <div style="background-color: #252525; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #0dcaf0;">
                        <h3 style="margin-top: 0; color: #ffffff;">{t.name}</h3>
                        <p style="margin-bottom: 5px;">📍 <strong>Location:</strong> {t.location}</p>
                        <p style="margin-bottom: 5px;">📅 <strong>Start Date:</strong> {t.start_date.strftime('%d %b %Y')}</p>
                        <p style="margin-bottom: 5px;">⏱️ <strong>Duration:</strong> {t.duration} Days</p>
                        <p style="margin-bottom: 0;">🎟️ <strong>Slots Reserved:</strong> {b.slots_booked}</p>
                    </div>
                    
                    <p>Please make sure to arrive at the reporting location on time with your gear. If you have any questions, reach out to your assigned guide or staff support.</p>
                    <p>Happy Trekking!<br><em>The Trekosphere Team</em></p>
                </div>
            </body>
            </html>
            """
            send_email(to_email, f"Reminder: Your trek '{t.name}' starts tomorrow!", html_content)
            count += 1
            
    return f"Daily reminder task completed. Sent {count} reminder email(s)."
