""" Models for the verification_code module. """

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import validates
from database import Base
from utils import (
    validate_email_field,
)


class VerificationCode(Base):
    """Verification code model"""

    __tablename__ = "verification_code"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(6), nullable=False)
    email = Column(String, nullable=False, index=True, unique=True)
    expires_at = Column(DateTime, nullable=False)
    is_validated = Column(Boolean, default=False)

    @validates("email")
    def validate_email(self, _, email):
        """
        Validates the email attribute.
        """
        return validate_email_field(email)
