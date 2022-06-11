import mongoengine as me


class User(me.Document):
    first_name = me.StringField(required=True)
    middle_name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    email = me.EmailField(required=True)
    role = me.StringField(required=True)
