from flask import Flask
import os
from dotenv import load_dotenv
from instance.config import app_config
from extensions import mongo
from v1 import v1
from v2 import v2

load_dotenv(".env")


def create_app(config: str):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config])
    app.register_blueprint(v1, url_prefix="/api/v1")
    app.register_blueprint(v2, url_prefix='/api/v2')

    app.config.from_pyfile('config.py')

    app.config["MONGO_URI"] = os.environ.get("DB_URI")

    mongo.init_app(app)

    return app


app = create_app(os.environ.get("CONFIG"))
