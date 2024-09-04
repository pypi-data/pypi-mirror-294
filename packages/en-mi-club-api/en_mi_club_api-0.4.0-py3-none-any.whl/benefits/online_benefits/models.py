""" This module contains the model for the OnlineBenefit table. """

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    func,
)
from sqlalchemy.orm import relationship
from database import Base


class OnlineBenefit(Base):
    """Model for the OnlineBenefit table."""

    __tablename__ = "online_benefits"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=True, default=None)
    is_valid = Column(Boolean, default=True)

    commerce_id = Column(
        Integer, ForeignKey("commerces.id", ondelete="CASCADE"), nullable=False
    )

    commerce = relationship("Commerce", back_populates="online_benefits")

    users = relationship(
        "UserOnlineBenefitAssociation",
        back_populates="benefit",
        cascade="all, delete-orphan",
    )


class UserOnlineBenefitAssociation(Base):
    """Association table for the many-to-many relationship between Users and OnlineBenefits."""

    __tablename__ = "user_onlinebenefit_associations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    online_benefit_id = Column(
        Integer, ForeignKey("online_benefits.id", ondelete="CASCADE")
    )
    created_at = Column(DateTime, nullable=False, default=func.now())
    expiration_date = Column(DateTime, nullable=False)
    code = Column(String(50), nullable=False)

    user = relationship("User", back_populates="online_benefits")
    benefit = relationship("OnlineBenefit", back_populates="users")
