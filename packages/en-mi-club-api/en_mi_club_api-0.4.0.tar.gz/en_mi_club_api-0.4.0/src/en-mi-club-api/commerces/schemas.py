""" Commerce schemas """

from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from utils import (
    validate_email_field,
    validate_rut,
    validate_chilean_phone_number,
)
from enums import DocumentType, Country


class CommerceBase(BaseModel):
    """Base schema for the Commerce model"""

    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: str = Field(None, min_length=1, max_length=15)
    document_type: DocumentType
    document_number: str = Field(..., min_length=11, max_length=12)
    country: Country
    address: str
    latitude: str
    longitude: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: EmailStr):
        """
        Validates the email attribute.
        """
        return validate_email_field(email)

    @field_validator("document_number")
    @classmethod
    def validate_rut(cls, document_number: str):
        """
        Validates the document_number attribute as a chilean rut.
        """
        validate_rut(document_number)
        return document_number

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone: str):
        """
        Validates the phone attribute.
        """
        validate_chilean_phone_number(phone)
        return phone


class CommerceCreate(CommerceBase):
    """Schema for creating a Commerce"""


class Commerce(CommerceBase):
    """Schema for the Commerce model"""

    model_config = ConfigDict(from_attributes=True)
    id: int
