""" Schemas for payment request module. """

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)
from enums import Currency
from .enums import Bank, AccountType


class PaymentRequestBase(BaseModel):
    """Base payment request schema."""

    bank: Bank
    account_type: AccountType
    account_number: str = Field(..., min_length=1, max_length=50)


class PaymentRequestCreate(PaymentRequestBase):
    """Schema to create a payment request."""


class PaymentRequest(PaymentRequestBase):
    """Payment request schema."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int = Field(..., ge=1)
    is_payed: bool
    currency: Currency = Currency.CLP
    amount: int = Field(default=0, ge=0)
