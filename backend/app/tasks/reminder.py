import datetime
from celery import shared_task
from app.models.trek import Trek
from app.models.booking import Booking
from app.services.email_service import send_email, render_email_template

@shared_task
def send_daily_reminders():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    
    treks = Trek.query.filter_by(start_date=tomorrow).filter(Trek.status.in_(["Approved", "Open", "Closed"])).all()
    
    count = 0
    for t in treks:
        ## get active bookings
        bookings = Booking.query.filter_by(trek_id=t.id, status=Booking.STATUS_BOOKED).all()
        for b in bookings:
            if not b.user:
                continue
            
            user_name = b.user.name
            to_email = b.user.email
            
 
            body_html = f"""
            <h2 style="color: #0891b2; margin-top: 0; margin-bottom: 16px; font-size: 20px; font-weight: 700; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">Upcoming Trek Reminder! 🏔️</h2>
            <p style="color: #fff; margin: 0 0 12px 0;">Hi <strong style="color: #0891b2;">{user_name}</strong>,</p>
            <p style="color: #fff; margin: 0 0 16px 0;">This is a friendly reminder that your upcoming adventure is starting tomorrow!</p>
            
            <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #00f2fe; border: 1px solid #e5e7eb; border-left: 4px solid #0891b2;">
                <h3 style="margin-top: 0; color: #0f172a; font-size: 16px; font-weight: bold; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">{t.name}</h3>
                <p style="margin-bottom: 8px; margin-top: 12px; color: #0891b2; font-size: 14px;">📍 <strong style="color: #0f172a;">Location:</strong> {t.location}</p>
                <p style="margin-bottom: 8px; color: #0891b2; font-size: 14px;">📅 <strong style="color: #0f172a;">Start Date:</strong> {t.start_date.strftime('%d %b %Y')}</p>
                <p style="margin-bottom: 8px; color: #0891b2; font-size: 14px;">⏱️ <strong style="color: #0f172a;">Duration:</strong> {t.duration} Days</p>
                <p style="margin-bottom: 0; color: #0891b2; font-size: 14px;">🎟️ <strong style="color: #0f172a;">Slots Reserved:</strong> {b.slots_booked}</p>
            </div>
            
            <p style="color: #fff; margin: 16px 0 0 0;">Please make sure to arrive at the reporting location on time with your gear. If you have any questions, reach out to your assigned guide or staff support.</p>
            """
            html_content = render_email_template(f"Reminder: {t.name}", body_html)
            send_email(to_email, f"Reminder: Your trek '{t.name}' starts tomorrow!", html_content)
            count += 1
            
    return f"Daily reminder task completed. Sent {count} reminder email(s)."
