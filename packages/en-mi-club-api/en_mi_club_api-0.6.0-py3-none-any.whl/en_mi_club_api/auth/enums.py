""" Enums for the auth module."""

from enum import Enum


class AccountType(str, Enum):
    """Account types"""

    USER = "User"
    ADMIN = "Admin"
