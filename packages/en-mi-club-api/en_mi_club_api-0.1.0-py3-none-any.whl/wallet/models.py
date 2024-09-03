""" Models for the wallet module. """

from sqlalchemy import (
    Column,
    Integer,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from database import Base
from enums import Currency


class Wallet(Base):
    """
    Wallet model
    """

    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Integer, nullable=False, default=0)
    currency = Column(SQLAlchemyEnum(Currency), nullable=False, name="currency")
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    user = relationship("User", back_populates="wallet", uselist=False)

    __table_args__ = (UniqueConstraint("user_id", name="uq_user_wallet"),)
