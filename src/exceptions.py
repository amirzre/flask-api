from http import HTTPStatus


class CustomException(Exception):
    """
    A custom exception class for general HTTP errors.
    """

    code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        """
        Initializes the exception with an optional custom message.
        """
        if message:
            self.message = message


class InternalException(CustomException):
    """
    Exception raised for HTTP 500 Internal Server Error.
    """

    code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = HTTPStatus.INTERNAL_SERVER_ERROR
    message = HTTPStatus.INTERNAL_SERVER_ERROR.description


class BadRequestException(CustomException):
    """
    Exception raised for HTTP 400 Bad Request.
    """

    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class NotFoundException(CustomException):
    """
    Exception raised for HTTP 404 Not Found.
    """

    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class UnauthorizedException(CustomException):
    """
    Exception raised for HTTP 401 Unauthorized.
    """

    code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description
