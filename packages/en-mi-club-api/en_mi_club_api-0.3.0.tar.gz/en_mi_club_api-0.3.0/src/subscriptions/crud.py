""" Crud operations for subscriptions. """

from datetime import datetime
from sqlalchemy.orm import Session
from plans import crud as plans_crud
from . import models, schemas, exceptions, enums


def create_empty_subscription(db: Session, user_id: int) -> models.Subscription:
    """
    Create a empty subscription. This function is used when a user is created.
    The created subscription will be pending.
    """

    db_subscription = models.Subscription(
        user_id=user_id,
        status=enums.Status.PENDING,
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def get_subscription_by_id_if_exists(
    db: Session, subscription_id: int
) -> models.Subscription | None:
    """Get a subscription by ID."""
    subscription = (
        db.query(models.Subscription)
        .filter(models.Subscription.id == subscription_id)
        .one_or_none()
    )
    return subscription


def get_subscription_by_id(
    db: Session, subscription_id: int
) -> models.Subscription:
    """Get a subscription by ID."""
    subscription = get_subscription_by_id_if_exists(db, subscription_id)
    if subscription is None:
        raise exceptions.SubscriptionNotFoundError()
    return subscription


def get_user_subscription(db: Session, user_id: int) -> models.Subscription:
    """Retrieve the subscription of a user."""
    return (
        db.query(models.Subscription)
        .filter(models.Subscription.user_id == user_id)
        .one_or_none()
    )


def activate_or_renew_subscription(
    db: Session, subscription_id: int, subscription: schemas.SubscriptionCreate
) -> models.Subscription:
    """
    Updates and activates a Subscription if the user wants to subscribe.
    Can be used to change the plan and/or the billing date.
    """
    plan = plans_crud.get_plan_by_id(db, subscription.plan_id)
    subscription.set_new_billing_at(plan.months_duration)
    db_subscription = get_subscription_by_id(db, subscription_id)
    for attr, value in subscription.model_dump(exclude_unset=True).items():
        setattr(db_subscription, attr, value)
    db_subscription.created_at = datetime.now()
    db_subscription.status = enums.Status.ACTIVE
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def subscribe(
    db: Session, user_id: int, subscription: schemas.SubscriptionCreate
) -> models.Subscription:
    """
    Subscribe a user to a plan.
    The subscription will be created if it doesn't exist (but it should),
    and it will be activated or renewed.
    """
    subscription_db = get_user_subscription(db, user_id)

    if not subscription_db:
        subscription_db = create_empty_subscription(db, user_id)

    return activate_or_renew_subscription(db, subscription_db.id, subscription)


def get_subscriptions(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.Subscription]:
    """Get all subscriptions."""
    return db.query(models.Subscription).offset(skip).limit(limit).all()


def delete_subscription(db: Session, subscription_id: int):
    """Delete a subscription."""
    db_subscription = get_subscription_by_id(db, subscription_id)
    db.delete(db_subscription)
    db.commit()
    return db_subscription
