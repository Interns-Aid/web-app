from flask_mail import Message

from core.extensions import mail


class EmailService:
    def __init__(self, email):
        self.email = email

    def send(self, token, title):
        msg = Message(
            title,
            sender="support@internsaid.com",
            recipients=[self.email],
            html=f"<a href='{token}'></a>",
        )
        mail.send(msg)
