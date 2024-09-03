""" CRUD operations for the users module. """

from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from user_entities.utils import hash_password
from user_entities.exceptions import EmailNotVerifiedError
from subscriptions.crud import create_empty_subscription
from wallet.crud import create_wallet
from wallet.schemas import WalletCreate
from verification_code.crud import (
    get_verification_code_by_email,
    delete_verification_code_by_email,
)
from . import models, schemas, exceptions, utils


def get_user_by_id(db: Session, user_id: int) -> models.User:
    """Get a user by ID."""
    user = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    if user is None:
        raise exceptions.UserNotFoundError()
    return user


def get_user_by_email_if_exists(db: Session, email: str) -> models.User | None:
    """Get a user by email."""
    user = (
        db.query(models.User).filter(models.User.email == email).one_or_none()
    )
    return user


def get_user_by_email(db: Session, email: str) -> models.User:
    """Get a user by email."""
    user = get_user_by_email_if_exists(db, email)
    if user is None:
        raise exceptions.UserNotFoundError()
    return user


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.User]:
    """Get all users."""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user.
    It will also create an empty subscription for the user.
    """
    code = get_verification_code_by_email(db, user.email)
    if not code.is_validated or code.expires_at < datetime.now():
        raise EmailNotVerifiedError()
    hashed_password = hash_password(user.password)
    db_user = models.User(
        **user.model_dump(exclude={"password"}, exclude_none=True),
        hashed_password=hashed_password
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise exceptions.DuplicateUserError from e
    except ValueError as e:
        db.rollback()
        raise e
    db.refresh(db_user)

    promocode = utils.generate_referral_code(db_user.id, db_user.name)
    db_user.promocode = promocode
    db.commit()

    create_empty_subscription(db=db, user_id=db_user.id)
    wallet_data = WalletCreate(user_id=db_user.id)
    create_wallet(db=db, wallet=wallet_data)
    delete_verification_code_by_email(db, user.email)

    return db_user


def delete_user(db: Session, user_id: int):
    """Delete a user."""
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()
    return db_user


def get_user_by_promocode(db: Session, promocode: str) -> models.User:
    """
    Retrieve a user by their promocode.
    Raises an HTTPException if the user is not found.
    """
    user = (
        db.query(models.User)
        .filter(models.User.promocode == promocode)
        .one_or_none()
    )

    if not user:
        raise exceptions.PromoCodeDoesntExistError()
    return user
