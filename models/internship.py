from core.extensions import db
from models.user import BaseModel


class Attachment(BaseModel):
    url = db.Column(db.String)
    internship_id = db.Column(db.String, db.ForeignKey("internship.id"))
    internship = db.relationship("Internship", back_populates="attachments")


class Tag(BaseModel):
    title = db.Column(db.String)
    internship_id = db.Column(db.String, db.ForeignKey("internship.id"))
    internship = db.relationship("Internship", back_populates="tags")


class Assignment(BaseModel):
    title = db.Column(db.String, nullable=False)
    duration = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    internship = db.relationship("Internship", back_populates="assignment")

    __mapper_args__ = {
        "polymorphic_identity": "assignment",
        "polymorphic_on": type,
    }


class Home(Assignment):
    id = db.Column(db.String, db.ForeignKey("assignment.id"), primary_key=True)
    description = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": "home",
    }


class Question(BaseModel):
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    coding_id = db.Column(db.String, db.ForeignKey("coding.id"))
    coding = db.relationship("Coding", back_populates="questions")


class Coding(Assignment):
    id = db.Column(db.String, db.ForeignKey("assignment.id"), primary_key=True)
    platform = db.Column(db.String)
    questions = db.relationship("Question", back_populates="coding")
    __mapper_args__ = {
        "polymorphic_identity": "coding",
    }


class Internship(BaseModel):
    title = db.Column(db.String, nullable=False)
    suggestion = db.Column(db.String)

    company_id = db.Column(db.ForeignKey("company.id"))
    company = db.relationship("Company", back_populates="internships")

    assigment_id = db.Column(db.ForeignKey("assignment.id"))
    assignment = db.relationship("Assignment", back_populates="internship")

    tags = db.relationship("Tag", back_populates="internship")
    attachments = db.relationship("Attachment", back_populates="internship")
