import os

import pydevd
from flask import Flask
from werkzeug.utils import import_string

from admin import admin
from core.extensions import migrate, db, ma, jwt
from errors import bp
from v1 import v1_bp


def create_app(config='config.DevelopmentConfig'):
    if os.environ.get('DEBUG') == 'true':
        pydevd.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True, suspend=False)
    app = Flask(__name__)
    cfg = import_string(config)()
    app.config.from_object(cfg)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    admin.init_app(app)
    app.register_blueprint(bp)
    app.register_blueprint(v1_bp, url_prefix="/api/v1")
    return app
