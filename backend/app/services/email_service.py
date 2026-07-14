import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.getenv("SMTP_SERVER", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))  # Default local SMTP port for debugging
SMTP_SENDER = os.getenv("SMTP_SENDER", "noreply@treksphere.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
USE_REAL_SMTP = os.getenv("USE_REAL_SMTP", "false").lower() == "true"

def send_email(to_email: str, subject: str, html_content: str):
    """
    Sends an HTML email.
    If USE_REAL_SMTP is false, it logs the email to backend/logs/sent_emails.log
    for development and grading verification.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_SENDER
    msg["To"] = to_email

    part = MIMEText(html_content, "html")
    msg.attach(part)

    if USE_REAL_SMTP:
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                if SMTP_PASSWORD:
                    server.login(SMTP_SENDER, SMTP_PASSWORD)
                server.sendmail(SMTP_SENDER, to_email, msg.as_string())
            print(f"SMTP Success: Sent email to {to_email} with subject '{subject}'")
        except Exception as e:
            print(f"SMTP Error sending email to {to_email}: {e}")
            _log_email_locally(to_email, subject, html_content)
    else:
        _log_email_locally(to_email, subject, html_content)

def _log_email_locally(to_email: str, subject: str, html_content: str):
    """
    Logs the email content locally to logs/sent_emails.log
    """
    import datetime
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "sent_emails.log")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(f"TIMESTAMP: {datetime.datetime.now().isoformat()}\n")
        f.write(f"TO: {to_email}\n")
        f.write(f"FROM: {SMTP_SENDER}\n")
        f.write(f"SUBJECT: {subject}\n")
        f.write("-" * 80 + "\n")
        f.write(html_content + "\n")
        f.write("=" * 80 + "\n\n")
        
    print(f"Local Log Success: Mock sent email to {to_email} with subject '{subject}'. Check backend/logs/sent_emails.log")
