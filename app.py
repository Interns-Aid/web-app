import os

import pydevd
from flask import Flask
from werkzeug.utils import import_string

from core.extensions import migrate, db, ma
from v1 import v1_bp


def create_app(config='config.TestingConfig'):
    if os.environ.get('DEBUG') == 'true':
        pydevd.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True, suspend=False)
    app = Flask(__name__)
    cfg = import_string(config)()
    app.config.from_object(cfg)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(v1_bp, url_prefix="/api/v1")
    return app
