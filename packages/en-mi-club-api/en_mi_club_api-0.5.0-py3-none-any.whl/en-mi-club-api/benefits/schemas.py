""" This module contains the schemas for the in-person benefits. """

from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, field_serializer
from utils import serialize_url


class BenefitBase(BaseModel):
    """Base schema for Benefits"""

    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1)
    commerce_id: int = Field(..., ge=1)
    image_url: Optional[HttpUrl] = None

    @field_serializer("image_url")
    def serialize_image_url(self, image_url: HttpUrl, _info):
        """
        Serializes the image_url attribute into a string.
        """
        return serialize_url(image_url)


class Benefit(BenefitBase):
    """Schema for Benefits"""

    is_valid: bool = True
    id: int
