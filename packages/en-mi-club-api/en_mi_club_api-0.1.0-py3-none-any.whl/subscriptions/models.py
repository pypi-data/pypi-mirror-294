""" Models for subscriptions. """

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Enum as SQLAlchemyEnum,
    func,
)
from sqlalchemy.orm import relationship

from database import Base
from .enums import Status


class Subscription(Base):

    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    new_billing_at = Column(DateTime, nullable=True)
    status = Column(SQLAlchemyEnum(Status), nullable=False, name="status")
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    plan_id = Column(
        Integer, ForeignKey("plans.id", ondelete="CASCADE"), nullable=True
    )

    user = relationship("User", back_populates="subscription", uselist=False)
    plan = relationship("Plan", back_populates="subscriptions")

    __table_args__ = (UniqueConstraint("user_id", name="uq_user_subscription"),)
