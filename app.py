import os

from flask import Flask
from mongoengine import *

from database import db


def create_app():
    app = Flask(__name__)
    print(os.environ.get(''))
    app.config['MONGODB_SETTINGS'] = {
        'host': f"mongodb://"
                f"{os.environ.get('DB_USER')}"
                f":{os.environ.get('DB_PASSWORD')}"
                f"@{os.environ.get('DB_HOST')}"
                f":{os.environ.get('DB_PORT')}"
                f"/{os.environ.get('DB_NAME')}?authSource=admin"
    }
    db.init_app(app)
    return app


app = create_app()


@app.get("/")
def home():
    return {"hello": "world"}


class User(Document):
    first_name = StringField(required=True)
    middle_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True)


@app.post("/users")
def create_user():
    user = User(first_name="Rajesh", middle_name="Kumar", last_name="Khadka", email="rajesh-kumar.khadka@epita.fr")
    user.save()
    return {"success": True}


@app.get("/users")
def list_users():
    return User.objects.to_json()
