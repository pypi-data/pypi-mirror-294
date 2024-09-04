""" Raffle model """

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Raffle(Base):
    """Raffle model"""

    __tablename__ = "raffles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    min_participants = Column(Integer, default=0)
    stream_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    winner_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    winner = relationship(
        "User", back_populates="raffles_won", foreign_keys=[winner_id]
    )
    tickets = relationship(
        "Ticket", back_populates="raffle", cascade="all, save-update"
    )
