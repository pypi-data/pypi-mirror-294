""" This module contains utility functions for the users entities. """

import re
from datetime import date
from passlib.context import CryptContext
from dateutil.relativedelta import relativedelta
from .constants import PASS_REGEX_PATTERN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_name(name: str, field: str):
    """
    Validates the name attribute.
    """
    if not name:
        raise ValueError(f"{field} must not be empty.")
    return name


# TODO: allow ñ in passwords
def validate_password(password: str):
    """
    Validates the password attribute.
    """
    if not re.match(PASS_REGEX_PATTERN, password):
        raise ValueError(
            "Password must contain at least one lowercase letter, "
            "one uppercase letter, one digit, and one special character."
        )
    return password


def validate_birth_date(birth_date: date):
    """
    Validates the birth_date attribute.
    """
    if birth_date > date.today() - relativedelta(years=18):
        raise ValueError("birth_date must be at least 18 years ago.")
    return birth_date


def hash_password(password: str) -> str:
    """Hash the password using the bcrypt algorithm."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the password using the bcrypt algorithm."""
    return pwd_context.verify(plain_password, hashed_password)
