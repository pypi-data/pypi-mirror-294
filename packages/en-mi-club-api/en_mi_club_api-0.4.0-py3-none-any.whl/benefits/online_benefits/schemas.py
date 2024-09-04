""" This module contains the schemas for the online benefits. """

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from benefits.schemas import BenefitBase, Benefit


class CreateOnlineBenefit(BenefitBase):
    """Schema for online benefit creation"""


class OnlineBenefit(Benefit):
    """Schema for online benefit"""

    model_config = ConfigDict(from_attributes=True)


class BaseUserOnlineBenefitAssociation(BaseModel):
    """Base Schema for the association between users and online benefits"""

    user_id: int
    online_benefit_id: int


class UserOnlineBenefitAssociation(BaseUserOnlineBenefitAssociation):
    """Schema for the association between users and online benefits"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    expiration_date: datetime
    code: str
