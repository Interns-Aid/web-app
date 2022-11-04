from flask_apispec import FlaskApiSpec
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
mail = Mail()
docs = FlaskApiSpec()
