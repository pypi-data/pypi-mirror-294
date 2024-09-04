""" Models for the payment request module. """

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Enum as SQLAlchemyEnum,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from database import Base
from enums import Currency
from .enums import Bank, AccountType


class PaymentRequest(Base):
    """
    Payment Request model
    """

    __tablename__ = "payment_requests"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False, default=0)
    currency = Column(SQLAlchemyEnum(Currency), nullable=False, name="currency")
    bank = Column(SQLAlchemyEnum(Bank), nullable=False)
    account_type = Column(SQLAlchemyEnum(AccountType), nullable=False)
    account_number = Column(String(50), nullable=False)
    is_payed = Column(Boolean, nullable=False, default=False)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    user = relationship("User", back_populates="payment_requests")
