from functools import wraps

from flask import session

from src.exceptions import UnauthorizedException


def login_required(fn):
    """
    Check that user autenticated.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            raise UnauthorizedException(message="Authentication required.")
        return fn(*args, **kwargs)

    return wrapper
