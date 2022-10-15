from core.extensions import db
from models.user import BaseModel


class Company(BaseModel):
    name = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    internships = db.relationship("Internship", back_populates="company")
