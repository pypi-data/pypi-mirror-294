"""User model."""

from sqlalchemy.orm import relationship, validates
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Enum as SQLAlchemyEnum,
)
from database import Base
from user_entities.utils import (
    validate_birth_date,
    validate_name,
)
from utils import (
    validate_email_field,
    validate_rut,
    validate_chilean_phone_number,
)
from enums import DocumentType, Country
from .enums import Gender


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=True, default=None)
    document_type = Column(SQLAlchemyEnum(DocumentType), nullable=False)
    document_number = Column(String(12), unique=True, nullable=False)
    birth_date = Column(Date, nullable=True, default=None)
    gender = Column(SQLAlchemyEnum(Gender), nullable=True, name="gender")
    image_url = Column(String, nullable=True, default=None)
    country = Column(SQLAlchemyEnum(Country), nullable=False, name="country")
    address = Column(String, nullable=True, default=None)
    latitude = Column(String, nullable=True, default=None)
    longitude = Column(String, nullable=True, default=None)
    promocode = Column(String, nullable=True, default=None)
    raffles_won = relationship(
        "Raffle", back_populates="winner", foreign_keys="[Raffle.winner_id]"
    )
    tickets = relationship(
        "Ticket",
        back_populates="user",
        foreign_keys="[Ticket.user_id]",
        cascade="all, delete-orphan",
    )

    online_benefits = relationship(
        "UserOnlineBenefitAssociation",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    in_person_benefits = relationship(
        "UserInPersonBenefitAssociation",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    subscription = relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )

    wallet = relationship(
        "Wallet",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )

    payment_requests = relationship(
        "PaymentRequest", back_populates="user", cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, _, name):
        """
        Validates the name attribute.
        """
        return validate_name(name, "name")

    @validates("last_name")
    def validate_last_name(self, _, last_name):
        """
        Validates the last_name attribute.
        """
        return validate_name(last_name, "last_name")

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

    @validates("birth_date")
    def validate_birth_date(self, _, birth_date):
        """
        Validates the birth_date attribute.
        """
        return validate_birth_date(birth_date)
