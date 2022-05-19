from flask import Flask
import os
from dotenv import load_dotenv
from werkzeug.utils import import_string
from extensions import mongo

load_dotenv(".env")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")
SECRET_KEY = os.environ.get("SECRET_KEY")


def create_app(config: str):
    app = Flask(__name__)
    app.config.from_object(import_string(config)())
    app.config["SECRET_KEY"] = SECRET_KEY
    mongo.init_app(app)

    return app


app = create_app(os.environ.get("CONFIG"))
