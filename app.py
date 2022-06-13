import os

from flask import Flask

from database import db
from v1 import v1_bp
import pydevd


def create_app():
    if os.environ.get('DEBUG') == 'true':
        pydevd.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True, suspend=False)
    app = Flask(__name__)
    app.config['MONGODB_HOST'] = os.environ.get("URI")
    db.init_app(app)
    app.register_blueprint(v1_bp, url_prefix="/api/v1")
    return app


app = create_app()


@app.get("/")
def home():
    return {"hello": "world-build-check"}
