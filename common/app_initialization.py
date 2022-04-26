from flask import Flask
from common.environ import environ


def create_app():
    app = Flask(__name__)

    if environ['ENV'] == 'DEV':
        app.config.from_object('config.ConfigDevelopment')

    if environ['ENV'] == 'TEST':
        app.config.from_object('config.ConfigTesting')

    return app
