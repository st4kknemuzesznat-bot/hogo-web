import os
from flask import Flask
app = Flask(__name__)
from dotenv import load_dotenv

from .config import Config
from .db import init_db


def create_app():
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config())

    # instance folder (SQLite)
    os.makedirs(app.instance_path, exist_ok=True)

    # uploads
    os.makedirs(app.config["EVENT_UPLOAD_DIR"], exist_ok=True)

    # init DB
    init_db(app)

    # routes
    from .routes import bp as public_bp
    from .auth import bp as auth_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)

    return app
