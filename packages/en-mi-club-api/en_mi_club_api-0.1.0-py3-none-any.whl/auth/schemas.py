""" This module contains the schemas for the authentication module. """

from datetime import timedelta, datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
from config import get_settings
from user_entities.utils import validate_password
from . import constants, enums

settings = get_settings()


class Token(BaseModel):
    """Schema for the token"""

    access_token: str


class TokenData(BaseModel):
    """Schema for the token data"""

    email: EmailStr
    is_admin: bool = False
    exp: datetime = Field(
        default_factory=lambda: datetime.now()
        + timedelta(minutes=settings.access_token_expire_minutes),
    )


class RecoverPasswordTokenData(BaseModel):
    """Schema for the recover password token"""

    email: EmailStr
    exp: datetime = Field(
        default_factory=lambda: datetime.now()
        + timedelta(minutes=constants.RECOVER_PASSWORD_TOKEN_EXPIRE_MINUTES),
    )
    account_type: enums.AccountType


class ResetPasswordRequest(BaseModel):
    """Schema for the reset password request"""

    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, new_password: str):
        """
        Validates the password attribute.
        """
        return validate_password(new_password)


class ChangePasswordRequest(ResetPasswordRequest):
    """Schema for the change password request"""

    old_password: str
