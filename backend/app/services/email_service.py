import os
from flask_mail import Message
from app.extensions import mail

SMTP_SENDER = os.getenv("SMTP_SENDER", "noreply@treksphere.app")
USE_REAL_SMTP = os.getenv("USE_REAL_SMTP", "false").lower() == "true"



def render_email_template(title: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0b0f19; color: #f3f4f6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
  <div class="wrapper" style="background-color: #0b0f19; padding: 30px 15px;">
    <div class="container" style="max-width: 580px; margin: 0 auto; background-color: #111827; border: 1px solid rgba(0, 242, 254, 0.25); border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5);">
      <div class="header" style="background: linear-gradient(135deg, #0b0f19 0%, #1e1b4b 100%); padding: 24px; text-align: center; border-bottom: 1px solid rgba(0, 242, 254, 0.15);">
        <div class="logo-container" style="display: inline-flex; align-items: center; justify-content: center;">
          <img class="logo-img" src="cid:logo" alt="Logo" style="height: 36px; width: auto; vertical-align: middle; margin-right: 12px;" />
          <span class="brand-name" style="font-size: 24px; font-weight: 800; letter-spacing: -0.025em; color: #00f2fe; margin: 0; vertical-align: middle; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">TrekSphere</span>
        </div>
      </div>
      <div class="content" style="padding: 32px 24px; color: #f3f4f6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 16px; line-height: 1.6;">
        {body_html}
      </div>
      <div class="footer" style="background-color: #0b0f19; padding: 24px; text-align: center; border-top: 1px solid rgba(255, 255, 255, 0.05); font-size: 11px; color: #9ca3af; line-height: 1.5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <p style="font-weight: bold; color: #f3f4f6; margin: 0 0 4px 0; font-size: 12px; letter-spacing: 0.05em; text-transform: uppercase;">TrekSphere</p>
        <p style="margin: 0 0 8px 0; color: #9ca3af;">Trekking Management App V2</p>
        <p style="margin: 0; color: #fff;">MAD-2 Course Project | Developed by Devendra Chouhan</p>
      </div>
    </div>
  </div>
</body>
</html>"""



def send_email(to_email: str, subject: str, html_content: str):
    logo_data = None
    if "cid:logo" in html_content:
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
        logo_path = os.path.join(static_dir, "logo.png")
        if os.path.exists(logo_path):
            try:
                with open(logo_path, "rb") as f:
                    logo_data = f.read()
            except Exception as e:
                print(f"Failed to read logo image: {e}")

    if USE_REAL_SMTP:
        try:
            msg = Message(
                subject=subject,
                recipients=[to_email],
                html=html_content
            )
            if logo_data:
                msg.attach(
                    filename="logo.png",
                    content_type="image/png",
                    data=logo_data,
                    disposition="inline",
                    headers={"Content-ID": "<logo>"}
                )
            mail.send(msg)
            print(f"Flask-Mail Success: Sent email to {to_email} with subject '{subject}'")
        except Exception as e:
            print(f"Flask-Mail Error sending email to {to_email}: {e}")
            _log_email_locally(to_email, subject, html_content, bool(logo_data))
    else:
        _log_email_locally(to_email, subject, html_content, bool(logo_data))



def _log_email_locally(to_email: str, subject: str, html_content: str, logo_attached: bool = False):
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
        f.write(f"INLINE LOGO ATTACHED: {logo_attached}\n")
        f.write("-" * 80 + "\n")
        f.write(html_content + "\n")
        f.write("=" * 80 + "\n\n")
        
    print(f"Local Log Success: Mock sent email to {to_email} with subject '{subject}'. Check backend/logs/sent_emails.log")
