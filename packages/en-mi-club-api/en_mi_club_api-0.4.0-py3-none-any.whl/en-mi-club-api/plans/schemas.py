""" Schemas for the Plan model. """

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)
from enums import Currency


class PlanBase(BaseModel):
    """Base schema for the Plan model"""

    name: str = Field(..., min_length=1, max_length=50)
    description: str
    tickets: int = Field(..., ge=1)
    max_amount_of_benefits_given: int = Field(
        ..., ge=1, description="Total benefits a user can get"
    )
    max_amont_of_uses_per_benefit_given: int = Field(
        ..., ge=1, description="Amount of the same benefit a user can get"
    )
    price: int = Field(..., ge=1)
    currency: Currency
    months_duration: int = Field(..., ge=1)

    @field_validator("months_duration")
    @classmethod
    def validate_months_duration(cls, months_duration):
        """Validate that months_duration is either 1 or 12."""
        if months_duration not in {1, 12}:
            raise ValueError("months_duration can only be 1 or 12.")
        return months_duration


class PlanCreate(PlanBase):
    """Schema to create Plans"""


class Plan(PlanBase):
    """Schema for the Plan model"""

    model_config = ConfigDict(from_attributes=True)
    id: int
