""" CRUD operations for the payment request module. """

from sqlalchemy.orm import Session
from wallet.crud import get_wallet_by_user_id
from . import models, exceptions, schemas


def create_payment_request(
    db: Session, user_id: int, payment_request: schemas.PaymentRequestCreate
) -> models.PaymentRequest:
    """
    Create a new payment request of a user.
    it's made with the whole balance of the user wallet.
    """
    wallet = get_wallet_by_user_id(db, user_id)

    if wallet.balance <= 0:
        raise exceptions.InsufficientFundsError()

    db_payment_request = models.PaymentRequest(
        user_id=user_id,
        amount=wallet.balance,
        currency=wallet.currency,
        **payment_request.model_dump(exclude_none=True)
    )

    wallet.balance = 0

    db.add(db_payment_request)
    db.commit()
    db.refresh(db_payment_request)
    return db_payment_request


def get_payment_request_by_id_if_exists(db: Session, payment_request_id: int):
    """Get a payment request by ID if exists."""
    return (
        db.query(models.PaymentRequest)
        .filter(models.PaymentRequest.id == payment_request_id)
        .one_or_none()
    )


def get_payment_request_by_id(db: Session, payment_request_id: int):
    """Get a payment request by ID."""
    db_payment_request = get_payment_request_by_id_if_exists(
        db, payment_request_id
    )
    if db_payment_request is None:
        raise exceptions.PaymentRequestNotFoundError()
    return db_payment_request


def get_payment_requests_by_user_id(
    db: Session, user_id: int
) -> list[models.PaymentRequest]:
    """Get a payment request by user ID."""
    return (
        db.query(models.PaymentRequest)
        .filter(models.PaymentRequest.user_id == user_id)
        .all()
    )


def get_payment_requests(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.PaymentRequest]:
    """Get all payment requests."""
    return db.query(models.PaymentRequest).offset(skip).limit(limit).all()


def get_not_payed_payment_requests(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.PaymentRequest]:
    """Get not payed payment requests."""
    return (
        db.query(models.PaymentRequest)
        .filter(models.PaymentRequest.is_payed == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_not_payed_payment_requests_by_user_id(
    db: Session, user_id: int
) -> list[models.PaymentRequest]:
    """Get not payed payment requests by user ID."""
    return (
        db.query(models.PaymentRequest)
        .filter(
            models.PaymentRequest.user_id == user_id,
            models.PaymentRequest.is_payed == False,
        )
        .all()
    )


def mark_payment_request_as_payed(
    db: Session, payment_request_id: int
) -> models.PaymentRequest:
    """Mark a payment request as payed."""
    db_payment_request = get_payment_request_by_id(db, payment_request_id)
    db_payment_request.is_payed = True
    db.commit()
    db.refresh(db_payment_request)
    return db_payment_request


def delete_payment_request(
    db: Session, payment_request_id: int
) -> models.PaymentRequest:
    """Delete a payment request."""
    db_payment_request = get_payment_request_by_id(db, payment_request_id)
    db.delete(db_payment_request)
    db.commit()
    return db_payment_request
