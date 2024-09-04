""" Endpoints for the subscriptions module. """

from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from database import get_db
from auth.middlewares import require_admin, require_user
from user_entities.admin.schemas import Admin as AdminSchema
from user_entities.users.schemas import User as UserSchema
from . import crud, schemas

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
)


# TODO: add payment flow when creating a subscription
@router.post(
    "/",
    response_model=schemas.Subscription,
)
def subscribe(
    subscription: schemas.SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(require_user),
):
    """Activate a subscription."""
    return crud.subscribe(
        db=db, user_id=current_user.id, subscription=subscription
    )


@router.get("/", response_model=list[schemas.Subscription])
def read_subscriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Get all subscriptions."""
    subscriptions = crud.get_subscriptions(db, skip=skip, limit=limit)
    return subscriptions


@router.get("/user", response_model=schemas.Subscription)
def read_user_subscription(
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(require_user),
):
    """Get all subscriptions for a user."""
    subscription = crud.get_user_subscription(db, current_user.id)
    return subscription


@router.get("/{subscription_id}", response_model=schemas.Subscription)
def read_subscription(
    subscription_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Get a subscription by id."""
    db_subscription = crud.get_subscription_by_id(
        db, subscription_id=subscription_id
    )
    return db_subscription


@router.delete("/{subscription_id}", response_model=schemas.Subscription)
def delete_subscription(
    subscription_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Delete a subscription by id."""
    db_subscription = crud.delete_subscription(db, subscription_id)
    return db_subscription
