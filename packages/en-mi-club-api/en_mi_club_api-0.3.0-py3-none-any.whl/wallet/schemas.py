""" Schemas for wallet module. """

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)
from enums import Currency


class WalletBase(BaseModel):
    """Base wallet schema."""

    currency: Currency = Currency.CLP


class WalletCreate(WalletBase):
    """Schema to create a wallet."""

    user_id: int = Field(..., ge=1)


class Wallet(WalletBase):
    """Wallet schema."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    balance: int = Field(default=0, ge=0)
    user_id: int = Field(..., ge=1)


class WalletUpdate(BaseModel):
    """Schema to update a wallet."""

    amount: int = Field(..., ge=1)
