from flask import current_app as app
from flask import render_template
from flask_mail import Message

from core.extensions import mail


def send_verification_email(token, first_name, email):
    url = f"{app.config.get('DOMAIN_URL')}/api/v1/email-verification?token={token}"
    html_template = render_template(
        "email-verification.html", user={"first_name": first_name, "url": url}
    )
    msg = Message(
        "Confirm your email to get started with Internsaid",
        sender=app.config.get("EMAIL_SENDER"),
        recipients=[email],
    )
    msg.html = html_template
    mail.send(msg)
