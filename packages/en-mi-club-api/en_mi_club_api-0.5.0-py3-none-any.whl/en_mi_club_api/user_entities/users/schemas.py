"""User schemas module."""

from typing import Optional
from datetime import date
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    field_serializer,
    field_validator,
    ConfigDict,
)
from utils import serialize_url
from raffles.schemas import Raffle
from user_entities.utils import (
    validate_password,
    validate_birth_date,
)
from utils import (
    validate_email_field,
    validate_rut,
    validate_chilean_phone_number,
)
from enums import DocumentType, Country
from .enums import Gender


class UserBase(BaseModel):
    """Base schema for the User model"""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = Field(None, min_length=1, max_length=15)
    document_type: DocumentType
    document_number: str = Field(..., min_length=11, max_length=12)
    birth_date: date
    gender: Optional[Gender] = None
    image_url: Optional[HttpUrl] = None
    country: Country
    address: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None

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

    @field_serializer("image_url")
    def serialize_image_url(self, image_url: HttpUrl, _info):
        """
        Serializes the image_url attribute into a string.
        """
        return serialize_url(image_url)

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, birth_date: date):
        """
        Validates the birth_date attribute.
        """
        return validate_birth_date(birth_date)


class UserCreate(UserBase):
    """Schema for creating a User"""

    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
        """
        Validates the password attribute.
        """
        return validate_password(password)


class User(UserBase):
    """Schema for the User model"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    promocode: Optional[str] = None


class UserWithRaffle(User):
    """Schema for the User model that contians the raffles won by the user"""

    raffles_won: list[Raffle]
