""" Contact form model. """

from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import validates
from database import Base
from utils import (
    validate_email_field,
    validate_chilean_phone_number,
)
from enums import Country


class ContactForm(Base):
    """Contact form model"""

    __tablename__ = "contact_form"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    country = Column(SQLAlchemyEnum(Country), nullable=False, name="country")
    email = Column(String, nullable=False)
    company = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=False)
    message = Column(String, nullable=False)
    is_answered = Column(Boolean, default=False)

    @validates("email")
    def validate_email(self, _, email):
        """
        Validates the email attribute.
        """
        return validate_email_field(email)

    @validates("phone")
    def validate_phone_is_chilean_phone(self, _, phone):
        """
        Validates the phone attribute.
        """
        validate_chilean_phone_number(phone)
        return phone
