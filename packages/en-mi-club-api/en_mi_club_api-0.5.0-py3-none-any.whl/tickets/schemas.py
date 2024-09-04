""" This module contains the schemas for the tickets. """

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TicketBase(BaseModel):
    """Base schema for the Ticket model"""

    user_id: int


class TicketCreate(TicketBase):
    """Schema for creating a Ticket"""


class Ticket(TicketBase):
    """Schema for the Ticket model"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    expires_at: datetime
    raffle_id: Optional[int] = None
