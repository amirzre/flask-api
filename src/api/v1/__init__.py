from flask import Blueprint

from src.api.v1 import auth, users


def create_v1_blueprint():
    """Create v1 blueprint and register routes."""
    bp = Blueprint("v1", __name__)

    bp.register_blueprint(users.user_bp, url_prefix="/users")
    bp.register_blueprint(auth.auth_bp, url_prefix="/auth")

    return bp
