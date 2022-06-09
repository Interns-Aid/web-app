import os

from flask import Flask
from mongoengine import *

from database import db
from v1 import v1_bp


def create_app():
    app = Flask(__name__)
    app.config['MONGODB_HOST'] = os.environ.get("URI")
    db.init_app(app)
    app.register_blueprint(v1_bp, url_prefix="/api/v1")
    return app


app = create_app()


@app.get("/")
def home():
    return {"hello": os.environ.get("URI")}


class User(Document):
    first_name = StringField(required=True)
    middle_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True)


class Question(Document):
    title = StringField(required=True)


@app.post("/users")
def create_user():
    user = User(first_name="Rajesh", middle_name="Kumar", last_name="Khadka", email="rajesh-kumar.khadka@epita.fr")
    user.save()
    return {"success": True}


@app.post("/questions")
def create_question():
    question = Question(title="new questions")
    question.save()
    return {"success": True}


@app.get("/questions")
def list_question():
    return Question.objects.to_json()


@app.get("/users")
def list_users():
    return User.objects.to_json()
