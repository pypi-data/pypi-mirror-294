""" Utils used all over the app """

import re
from pydantic import HttpUrl
from rut_chile import rut_chile
from email_validator import validate_email, EmailNotValidError


def serialize_url(url: HttpUrl) -> str | None:
    """
    If exists, serializes the url given into a string.
    """
    if url is None:
        return None
    return str(url)


def validate_email_field(email: str):
    """
    Validates the email attribute.
    """
    try:
        validate_email(email, check_deliverability=True)
    except EmailNotValidError as e:
        raise ValueError("Invalid email.") from e
    return email


def validate_chilean_phone_number(number: str):
    """
    Validates a Chilean phone number.
    """
    if not re.match(r"^\+?56 \d{1} \d{4} \d{4}$", number):
        raise ValueError("phone must be in the format '+56 X XXXX XXXX'.")
    return number


def validate_rut(rut: str):
    """
    Validates a Chilean RUT.
    """
    if not re.match(r"^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$", rut):
        raise ValueError("rut must be in the format 'XX.XXX.XXX-X'.")
    if not rut_chile.is_valid_rut(rut.upper()):
        raise ValueError("rut is not valid.")
    return rut
