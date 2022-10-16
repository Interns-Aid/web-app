class EmailService:
    def __init__(self, email):
        self.email = email

    def send(self):
        return {"message": f"Email sent to {self.email}"}
