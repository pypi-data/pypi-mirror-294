""" Commerce models """

from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, validates
from database import Base
from enums import DocumentType, Country
from utils import (
    validate_email_field,
    validate_rut,
    validate_chilean_phone_number,
)


class Commerce(Base):
    """Commerce model"""

    __tablename__ = "commerces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    phone = Column(String(15), nullable=False)
    country = Column(SQLAlchemyEnum(Country), nullable=False, name="country")
    document_type = Column(SQLAlchemyEnum(DocumentType), nullable=False)
    document_number = Column(String(12), unique=True, nullable=False)

    accounts = relationship(
        "CommerceAccount",
        back_populates="commerce",
        cascade="all, delete-orphan",
    )

    online_benefits = relationship(
        "OnlineBenefit",
        back_populates="commerce",
        cascade="all, delete-orphan",
    )

    in_person_benefits = relationship(
        "InPersonBenefit",
        back_populates="commerce",
        cascade="all, delete-orphan",
    )

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

    @validates("document_number")
    def validate_rut_input(self, _, document_number):
        """
        Validates the rut attribute.
        """
        validate_rut(document_number)
        return document_number
