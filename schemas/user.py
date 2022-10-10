import re

from marshmallow import validates, post_load, fields, ValidationError, EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from werkzeug.security import generate_password_hash

from models.user import User


class UserSchema(SQLAlchemyAutoSchema):
    password = fields.Str(required=True)

    class Meta:
        model = User
        load_instance = True
        transient = True
        exclude = ('active',)
        load_only = ('password',)
        dump_only = ('id',)
        unknown = EXCLUDE

    @validates('password')
    def validate_password(self, value):
        password_regex = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
        if not re.match(password_regex, value):
            raise ValidationError('invalid password')

    @post_load
    def hash_password(self, data, **kwargs):
        data['password'] = generate_password_hash(data.get('password'))
        return data
