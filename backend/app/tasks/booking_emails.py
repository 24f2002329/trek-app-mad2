from celery import shared_task
from app.models.user import User
from app.models.booking import Booking
from app.services.email_service import send_email, render_email_template


@shared_task
def send_booking_confirmation_email(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return "Error: Booking not found."
    user = booking.user
    trek = booking.trek
    if not user or not trek:
        return "Error: User or Trek not found."
        
    start_str = trek.start_date.strftime('%d-%b-%Y') if trek.start_date else "N/A"
    
    body_html = f"""
    <h2 style="color: #0891b2; margin-top: 0; margin-bottom: 16px; font-size: 20px; font-weight: 700; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">Booking Confirmed! 🏕️</h2>
    <p style="color: #fff; margin: 0 0 12px 0;">Hi <strong style="color: #0891b2;">{user.name}</strong>,</p>
    <p style="color: #fff; margin: 0 0 16px 0;">Your trekking adventure has been successfully reserved. Here are the booking details:</p>
    <table style="width: 100%; border-collapse: collapse; margin-top: 20px; margin-bottom: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <tr style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 12px 0; font-weight: bold; color: #fff; font-size: 14px;">Trek Name</td>
            <td style="padding: 12px 0; text-align: right; font-weight: bold; color: #0f172a; font-size: 14px;">{trek.name}</td>
        </tr>
        <tr style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 12px 0; font-weight: bold; color: #fff; font-size: 14px;">Location</td>
            <td style="padding: 12px 0; text-align: right; color: #fff; font-size: 14px;">{trek.location}</td>
        </tr>
        <tr style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 12px 0; font-weight: bold; color: #fff; font-size: 14px;">Start Date</td>
            <td style="padding: 12px 0; text-align: right; color: #0891b2; font-weight: bold; font-size: 14px;">{start_str}</td>
        </tr>
        <tr style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 12px 0; font-weight: bold; color: #fff; font-size: 14px;">Slots Reserved</td>
            <td style="padding: 12px 0; text-align: right; color: #fff; font-size: 14px;">{booking.slots_booked}</td>
        </tr>
        <tr style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 12px 0; font-weight: bold; color: #fff; font-size: 14px;">Payment Status</td>
            <td style="padding: 12px 0; text-align: right; font-weight: bold; color: #b45309; font-size: 14px;">{booking.payment_status}</td>
        </tr>
    </table>
    <p style="color: #fff; margin: 0 0 16px 0;">Please complete your payment from the dashboard if it is pending.</p>
    <p style="margin-top: 24px; margin-bottom: 0; color: #fff;">See you on the trek!<br><em style="color: #fff;">The TrekSphere Team</em></p>
    """
    
    html_content = render_email_template("Booking Confirmed", body_html)
    send_email(user.email, f"TrekSphere: Booking Confirmed for {trek.name}", html_content)
    return f"Success: Booking confirmation sent to {user.email}"



@shared_task
def send_booking_cancellation_email(user_email, user_name, trek_name):
    body_html = f"""
    <h2 style="color: #dc2626; margin-top: 0; margin-bottom: 16px; font-size: 20px; font-weight: 700; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">Booking Cancelled ❌</h2>
    <p style="color: #fff; margin: 0 0 12px 0;">Hi <strong style="color: #0891b2;">{user_name}</strong>,</p>
    <p style="color: #fff; margin: 0 0 16px 0;">This email confirms that your booking for the trek <strong style="color: #0891b2;">{trek_name}</strong> has been cancelled successfully.</p>
    <p style="color: #fff; margin: 0 0 16px 0;">If this was a mistake or you wish to reserve another trek, please visit the TrekSphere dashboard.</p>
    <p style="margin-top: 24px; margin-bottom: 0; color: #fff;">Thank you,<br><em style="color: #fff;">The TrekSphere Team</em></p>
    """
    html_content = render_email_template("Booking Cancelled", body_html)
    send_email(user_email, f"TrekSphere: Cancellation Confirmation for {trek_name}", html_content)
    return f"Success: Booking cancellation sent to {user_email}"



@shared_task
def send_payment_confirmation_email(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return "Error: Booking not found."
    user = booking.user
    trek = booking.trek
    if not user or not trek:
        return "Error: User or Trek not found."
        
    body_html = f"""
    <h2 style="color: #0d9488; margin-top: 0; margin-bottom: 16px; font-size: 20px; font-weight: 700; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">Payment Received! 💳</h2>
    <p style="color: #fff; margin: 0 0 12px 0;">Hi <strong style="color: #0891b2;">{user.name}</strong>,</p>
    <p style="color: #fff; margin: 0 0 16px 0;">Thank you! Your payment for the trek <strong style="color: #0891b2;">{trek.name}</strong> has been successfully processed.</p>
    <p style="color: #fff; margin: 0 0 16px 0;">Your booking is now fully confirmed and marked as <strong style="color: #0d9488;">Paid</strong>.</p>
    <p style="margin-top: 24px; margin-bottom: 0; color: #fff;">Happy Trekking!<br><em style="color: #fff;">The TrekSphere Team</em></p>
    """
    html_content = render_email_template("Payment Confirmed", body_html)
    send_email(user.email, f"TrekSphere: Payment Confirmed for {trek.name}", html_content)
    return f"Success: Payment confirmation sent to {user.email}"
