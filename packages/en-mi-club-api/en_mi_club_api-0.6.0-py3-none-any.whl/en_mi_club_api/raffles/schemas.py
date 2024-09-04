"""Raffles schemas module."""

from typing import Optional
from datetime import datetime, timedelta
from pydantic import (
    BaseModel,
    field_serializer,
    HttpUrl,
    ValidationInfo,
    field_validator,
    ConfigDict,
    Field,
)
from utils import serialize_url
from tickets.schemas import Ticket
from . import constants


class RaffleBase(BaseModel):
    """Base schema for the Raffle model"""

    name: str
    description: str
    min_participants: Optional[int] = 0
    stream_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @field_serializer("image_url")
    def serialize_image_url(self, image_url: HttpUrl, _info):
        """
        Serializes the image_url attribute into a string.
        """
        return serialize_url(image_url)

    @field_serializer("stream_url")
    def serialize_stream_url(self, stream_url: HttpUrl, _info):
        """
        Serializes the stream_url attribute into a string.
        """
        return serialize_url(stream_url)

    @field_validator("end_date")
    @classmethod
    def validate_dates(
        cls, end_date: Optional[datetime], values: ValidationInfo
    ):
        """
        Validates that the end_date is at least 24 hours after start_date.
        """
        start_date = values.data.get("start_date")
        if (
            start_date
            and end_date
            and end_date <= start_date + timedelta(hours=constants.HOURS)
        ):
            raise ValueError(
                f"""
                end_date must be at least {constants.HOURS}
                hours after start_date.
                """
            )
        return end_date


class RaffleCreate(RaffleBase):
    """Schema to create Raffles"""


class Raffle(RaffleBase):
    """Schema for the Raffle model"""

    model_config = ConfigDict(from_attributes=True)
    id: int


class RaffleWinner(Raffle):
    """Schema for the Raffle that contains the winner"""

    winner_id: Optional[int] = None


class RaffleTickets(Raffle):
    """Schema for the Raffle model that contains the tickets"""

    tickets: list[Ticket]


class RaffleAssignment(BaseModel):
    """Schema for assigning a ticket to a raffle"""

    raffle_id: int = Field(
        ..., ge=1, description="ID of the raffle to assign the ticket to"
    )
