""" Endpoints for payment requests module. """

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from database import get_db
from auth.middlewares import require_admin, require_user
from user_entities.users import schemas as user_schemas
from user_entities.admin import schemas as admin_schemas
from . import schemas, crud

router = APIRouter(
    prefix="/payment_requests",
    tags=["payment_requests"],
)


@router.post(
    "/",
    response_model=schemas.PaymentRequest,
)
def create_payment_request(
    payment_request: schemas.PaymentRequestCreate,
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(require_user),
):
    """Create a new payment request."""
    return crud.create_payment_request(db, current_user.id, payment_request)


@router.get(
    "/",
    response_model=list[schemas.PaymentRequest],
)
def get_payment_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: admin_schemas.Admin = Depends(require_admin),
):
    """Get all payment requests."""
    return crud.get_payment_requests(db, skip=skip, limit=limit)


@router.get(
    "/not_payed",
    response_model=list[schemas.PaymentRequest],
)
def get_not_payed_payment_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: admin_schemas.Admin = Depends(require_admin),
):
    """Get not payed payment requests."""
    return crud.get_not_payed_payment_requests(db, skip=skip, limit=limit)


@router.get(
    "/user",
    response_model=list[schemas.PaymentRequest],
)
def get_payment_requests_by_user_id(
    current_user: user_schemas.User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Get all payment requests of a user."""
    return crud.get_payment_requests_by_user_id(db, current_user.id)


@router.get(
    "/{payment_request_id}",
    response_model=schemas.PaymentRequest,
)
def get_payment_request(
    payment_request_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: admin_schemas.Admin = Depends(require_admin),
):
    """Get a payment request by ID."""
    return crud.get_payment_request_by_id(db, payment_request_id)


@router.put(
    "/{payment_request_id}",
    response_model=schemas.PaymentRequest,
)
def mark_payment_request_as_payed(
    payment_request_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: admin_schemas.Admin = Depends(require_admin),
):
    """Mark a payment request as payed."""
    return crud.mark_payment_request_as_payed(db, payment_request_id)
