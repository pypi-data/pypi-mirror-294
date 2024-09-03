""" Admin schemas """

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from user_entities.utils import validate_password
from utils import validate_email_field


class AdminBase(BaseModel):
    """Base schema for the Admin model"""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=50)

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: EmailStr):
        """
        Validates the email attribute.
        """
        return validate_email_field(email)


class AdminCreate(AdminBase):
    """Schema for creating an Admin"""

    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
        """
        Validates the password attribute.
        """
        return validate_password(password)


class Admin(AdminBase):
    """Schema for the Admin model"""

    model_config = ConfigDict(from_attributes=True)
    id: int
