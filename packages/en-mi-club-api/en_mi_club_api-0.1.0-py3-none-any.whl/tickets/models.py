"""This module contains the Ticket model."""

from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from . import constants


class Ticket(Base):
    """Ticket model"""

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    raffle_id = Column(
        Integer, ForeignKey("raffles.id", ondelete="SET NULL"), nullable=True
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    expires_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now()
        + relativedelta(months=constants.TICKET_EXPIRATION_MONTHS),
    )

    user = relationship("User", back_populates="tickets")
    raffle = relationship("Raffle", back_populates="tickets")
