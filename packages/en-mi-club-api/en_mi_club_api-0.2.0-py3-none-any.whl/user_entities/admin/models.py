"""This module contains the Admin model."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from database import Base
from user_entities.utils import validate_name
from utils import validate_email_field


class Admin(Base):
    """Admin model"""

    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String(50), nullable=False)

    @validates("name")
    def validate_name(self, _, name):
        """
        Validates the name attribute.
        """
        return validate_name(name, "name")

    @validates("email")
    def validate_email(self, _, email):
        """
        Validates the email attribute.
        """
        return validate_email_field(email)
