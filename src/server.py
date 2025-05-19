from flask import Flask, jsonify

from src.api import register_blueprints
from src.config import config
from src.exceptions import CustomException
from src.extensions import db, migrate
from src.logging import register_request_logging


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(CustomException)
    def handle_custom_exception(exc: CustomException):
        payload = {
            "message": exc.message,
            "code": exc.error_code,
        }
        return jsonify(payload), exc.code


def create_app():
    """Application-factory pattern."""

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
    app.config["SECRET_KEY"] = config.SECRET_KEY

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)
    register_error_handlers(app)
    register_request_logging(app)

    return app


app = create_app()
