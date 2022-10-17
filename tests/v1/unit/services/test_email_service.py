from core.extensions import mail
from services.email import EmailService


def test_email_send(app):
    email_service = EmailService("support@internsaid.com")
    email_title = "Welcome"
    email_service.send("test_token", title=email_title)
    with mail.record_messages() as outbox:
        assert len(outbox) == 1
        assert outbox[0].subject == email_title
