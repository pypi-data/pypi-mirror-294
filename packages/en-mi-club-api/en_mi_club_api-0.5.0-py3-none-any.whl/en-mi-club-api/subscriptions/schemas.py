""" Schemas for subscriptions. """

from typing import Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, ConfigDict, Field
from .enums import Status


class SubscriptionBase(BaseModel):
    """Base schema for the Subscription model"""

    plan_id: Optional[int] = Field(..., ge=1)


class SubscriptionCreate(SubscriptionBase):
    """Schema to create Subscriptions"""

    new_billing_at: Optional[datetime] = Field(default=None)

    def set_new_billing_at(self, duration: int):
        """Set the new_billing_at based on the plan duration."""
        self.new_billing_at = datetime.now() + relativedelta(months=duration)


class Subscription(SubscriptionBase):
    """Schema for the Subscription model"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    new_billing_at: Optional[datetime]
    user_id: int = Field(..., ge=1)
    status: Status
