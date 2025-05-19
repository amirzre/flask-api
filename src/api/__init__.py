from flask import Blueprint, Flask

from src.api.v1 import create_v1_blueprint


def register_blueprints(app: Flask):
    """Register all blueprints."""

    v1_blueprint = create_v1_blueprint()
    app.register_blueprint(v1_blueprint, url_prefix="/api/v1")
