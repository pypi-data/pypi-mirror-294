""" Schemas for the contact form module. """

from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from utils import (
    validate_email_field,
    validate_chilean_phone_number,
)
from enums import Country


class ContactFormBase(BaseModel):
    """Base schema for the ContactForm model"""

    name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    country: Country
    email: EmailStr
    company: str = Field(..., min_length=1, max_length=50)
    phone: str = Field(..., min_length=1, max_length=15)
    message: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: EmailStr):
        """
        Validates the email attribute.
        """
        return validate_email_field(email)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone: str):
        """
        Validates the phone attribute.
        """
        validate_chilean_phone_number(phone)
        return phone


class ContactFormCreate(ContactFormBase):
    """Schema for creating a ContactForm"""


class ContactForm(ContactFormBase):
    """Schema for the ContactForm model"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    is_answered: bool


class ContactFormUpdate(BaseModel):
    """Schema for updating a ContactForm"""

    is_answered: bool
