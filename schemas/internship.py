from marshmallow_oneofschema import OneOfSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from models import Internship, Company
from models.internship import Tag, Attachment, Home, Question, Coding


class CompanySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True
        transient = True
        dump_only = ('id',)


class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True
        transient = True
        dump_only = ('id',)


class AttachmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Attachment
        load_instance = True
        transient = True
        dump_only = ('id',)


class QuestionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        load_instance = True
        transient = True
        dump_only = ('id',)


class CodingSchema(SQLAlchemyAutoSchema):
    questions = Nested(QuestionSchema, many=True)

    class Meta:
        model = Coding
        load_instance = True
        transient = True
        dump_only = ('id',)


class HomeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Home
        load_instance = True
        transient = True
        dump_only = ('id',)


class AssignmentSchema(OneOfSchema):
    type_schemas = {"coding": CodingSchema, "home": HomeSchema}

    def get_obj_type(self, obj):
        if isinstance(obj, Home):
            return "home"
        elif isinstance(obj, Coding):
            return "coding"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class InternshipSchema(SQLAlchemyAutoSchema):
    company = Nested(CompanySchema)
    tags = Nested(TagSchema, many=True)
    attachments = Nested(AttachmentSchema, many=True)
    assignment = Nested(AssignmentSchema, required=True)

    class Meta:
        model = Internship
        include_relationships = True
        load_instance = True
        transient = True
        dump_only = ('id',)
