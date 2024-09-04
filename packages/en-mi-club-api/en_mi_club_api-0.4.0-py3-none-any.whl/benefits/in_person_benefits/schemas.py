""" This module contains the schemas for the in-person benefits. """

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from benefits.schemas import BenefitBase, Benefit


class CreateInPersonBenefit(BenefitBase):
    """Schema for in person benefit creation"""


class InPersonBenefit(Benefit):
    """Schema for in person benefit"""

    model_config = ConfigDict(from_attributes=True)


class BaseUserInPersonBenefitAssociation(BaseModel):
    """Base Schema for the association between users and in person benefits"""

    user_id: int
    in_person_benefit_id: int


class UserInPersonBenefitAssociation(BaseUserInPersonBenefitAssociation):
    """Schema for the association between users and in person benefits"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    benefit: InPersonBenefit
