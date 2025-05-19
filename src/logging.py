from flask import Flask, request, session

from src.controllers import LogController
from src.schemas import CreateLog

log_controller = LogController()


def register_request_logging(app: Flask):
    """
    Attach an after_request hook to the app that writes every
    authenticated user's action into the logs table.
    """

    @app.after_request
    def log_request(response):
        user_id = session.get("user_id")
        if user_id:
            log_request = CreateLog(
                method=request.method,
                endpoint=request.path,
                status=str(response.status_code),
                user_id=user_id,
            )

            log_controller.create_log(log_request)

        return response
