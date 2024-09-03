""" Schemas for the verification_code module. """

from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from datetime import datetime
from datetime import timedelta
from utils import (
    validate_email_field,
)
from .utils import generate_six_digit_code
from .constants import MINUTES_TO_EXPIRE


class VerificationCodeBase(BaseModel):
    """Base schema for the VerificationCode model"""

    code: str = Field(
        ..., min_length=6, max_length=6, default_factory=generate_six_digit_code
    )
    expires_at: datetime = Field(
        ...,
        default_factory=lambda: datetime.now()
        + timedelta(minutes=MINUTES_TO_EXPIRE),
    )
    email: EmailStr

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: EmailStr):
        """
        Validates the email attribute.
        """
        return validate_email_field(email)


class VerificationCodeCreate(VerificationCodeBase):
    """Schema for creating a VerificationCode"""


class VerificationCode(VerificationCodeBase):
    """Schema for the VerificationCode model"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    is_validated: bool
