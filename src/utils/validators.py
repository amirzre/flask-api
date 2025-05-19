import re
from typing import Annotated

from pydantic import AfterValidator

from src.exceptions import BadRequestException


def validate_password(value: str) -> str:
    """
    Validates the strength of a password using a regex pattern.

    Ensures the password has at least:
    - 8 characters
    - One uppercase letter
    - One lowercase letter
    - One digit
    - One special character

    Args:
        value (str): The password string to validate.

    Raises:
        BadRequestException: If the password does not meet the required complexity.

    Returns:
        str: The validated password string.
    """
    password_pattern = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )

    if not password_pattern.match(value):
        raise BadRequestException(
            message=(
                "Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one number, and one special character."
            )
        )

    return value


def validate_phone(value: str) -> str:
    """
    Validates the strength of a phone number using a regex pattern.

    Ensures the phone number has at least:
    - 11 characters
    - Start with 09

    Args:
        value (str): The phone number string to validate.

    Raises:
        BadRequestException: If the phone number does not meet the required complexity.

    Returns:
        str: The validated phone number string.
    """
    phone_pattern = re.compile(r"^09\d{9}$")

    if not phone_pattern.match(value):
        raise BadRequestException(message="Invalid phone number.")

    return value


PasswordValidator = Annotated[str, AfterValidator(validate_password)]
PhoneValidator = Annotated[str, AfterValidator(validate_phone)]
