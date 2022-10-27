import uuid

from core.extensions import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.String, primary_key=True)

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)
        self.id = str(uuid.uuid4())


class User(BaseModel):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    active = db.Column(db.Boolean, default=False)
    # email_verified = db.Column(db.Boolean, default=False)
