from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask('Flask REST API', instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes import api_bp
    app.register_blueprint(api_bp)
    return app