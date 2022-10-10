from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from core.extensions import db
from models.user import User

admin = Admin(name='InternsAid')
admin.add_view(ModelView(User, db.session))
