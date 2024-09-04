""" This module contains the model for the InPersonBenefit table. """

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


class InPersonBenefit(Base):
    """Model for the InPersonBenefit table."""

    __tablename__ = "in_person_benefits"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=True, default=None)
    is_valid = Column(Boolean, default=True)

    commerce_id = Column(
        Integer, ForeignKey("commerces.id", ondelete="CASCADE"), nullable=False
    )

    commerce = relationship("Commerce", back_populates="in_person_benefits")

    users = relationship(
        "UserInPersonBenefitAssociation",
        back_populates="benefit",
        cascade="all, delete-orphan",
    )


class UserInPersonBenefitAssociation(Base):
    """Association table for the many-to-many relationship between Users and InPersonBenefits."""

    __tablename__ = "user_inpersonbenefit_associations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    in_person_benefit_id = Column(
        Integer, ForeignKey("in_person_benefits.id", ondelete="CASCADE")
    )
    created_at = Column(DateTime, nullable=False, default=func.now())

    user = relationship("User", back_populates="in_person_benefits")
    benefit = relationship("InPersonBenefit", back_populates="users")
