import os
import warnings

import pydevd
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from werkzeug.utils import import_string

from admin import admin
from config import TestingConfig
from core.extensions import migrate, ma, mail, docs
from errors import error_bp
from v1 import v1_bp
from v1.api_docs import add_docs
from v1.routes import *


def create_app(config="config.DevelopmentConfig"):
    if os.environ.get("DEBUG") == "true":
        pydevd.settrace(
            "host.docker.internal",
            port=12345,
            stdoutToServer=True,
            stderrToServer=True,
            suspend=False,
        )
    app = Flask(__name__, template_folder="templates/")

    cfg = import_string(config)()
    app.config.from_object(cfg)
    if not isinstance(cfg, TestingConfig):
        mail_settings = {
            "MAIL_SERVER": "smtp.gmail.com",
            "MAIL_PORT": 465,
            "MAIL_USE_TLS": False,
            "MAIL_USE_SSL": True,
            "MAIL_USERNAME": os.environ.get("MAIL_USERNAME"),
            "MAIL_PASSWORD": os.environ.get("MAIL_PASSWORD"),
        }
        app.config.update(mail_settings)

    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    admin.init_app(app)
    docs.init_app(app)
    app.config.update(
        {
            "APISPEC_SPEC": APISpec(
                title="InternsAID",
                version="v1",
                openapi_version="3.0.1",
                plugins=[MarshmallowPlugin()],
            ),
            "APISPEC_SWAGGER_URL": "/swagger/",
        }
    )

    warnings.filterwarnings("ignore", message="Multiple schemas resolved to the name")

    app.register_blueprint(error_bp)
    app.register_blueprint(v1_bp, url_prefix="/api/v1")

    add_docs(cfg)
    return app
