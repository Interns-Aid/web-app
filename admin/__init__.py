from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from core.extensions import db
from models.company import Company
from models.internship import Internship, Assignment, Home, Coding, Question
from models.user import User

admin = Admin(name="InternsAid", template_mode="bootstrap4")
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Company, db.session))
admin.add_view(ModelView(Internship, db.session))
admin.add_view(ModelView(Assignment, db.session))
admin.add_view(ModelView(Home, db.session))
admin.add_view(ModelView(Coding, db.session))
admin.add_view(ModelView(Question, db.session))
