""" Models for the plans app. """

from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from database import Base
from enums import Currency


class Plan(Base):
    """
    Plan model
    Attrs:
    - id: Plan id
    - name: Plan name
    - description: Plan description
    - tickets: Amount of tickets given to the user per month
    - max_amount_of_benefits_given: Total benefits a user can get in a month
    - max_amont_of_uses_per_benefit_given: Amount of the same benefit a user can get in a month
    - price: Plan price
    - currency: Plan currency
    - months_duration: Plan duration, can be 1 or 12 months
    """

    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String, nullable=False)
    tickets = Column(Integer, nullable=False)
    max_amount_of_benefits_given = Column(Integer, nullable=False)
    max_amont_of_uses_per_benefit_given = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    currency = Column(SQLAlchemyEnum(Currency), nullable=False, name="currency")
    months_duration = Column(Integer, nullable=False)

    subscriptions = relationship("Subscription", back_populates="plan")
