from flask import Flask
from common.environ import environ
from extensions import mongo


db_password = environ["DB_PASSWORD"]
db_name = environ["DB_NAME"]


def create_app():
    app = Flask(__name__)

    if environ['ENV'] == 'DEV':
        app.config.from_object('config.ConfigDevelopment')

    if environ['ENV'] == 'TEST':
        app.config.from_object('config.ConfigTesting')

    app.config["MONGO_URI"] = "mongodb+srv://krishna:db_password@cluster0.7oic7.mongodb.net/db_name?retryWrites=true&w=majority"

    mongo.init_app(app)

    return app
