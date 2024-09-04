""" Endpoints for the verification_code module. """

from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from database import get_db
from auth.middlewares import require_admin
from user_entities.admin.schemas import Admin

# import notifications.mailer.ses_service_functions as mailer
from . import crud, schemas


router = APIRouter(
    prefix="/verification_codes",
    tags=["verification_codes"],
)


@router.post(
    "/",
    response_model=schemas.VerificationCode,
)
def create_or_refresh_verification_code(
    email: str = Query(...),
    db: Session = Depends(get_db),
):
    """
    Create a new verification code or refresh it if it exists based on email.
    """
    code = crud.create_or_refresh_verification_code(db, email)
    print(code.code)
    # Send the verification code to the user's email.
    # TODO: fix before uncomment:
    # mailer.send_email_with_verification_code(code.email, code.code)

    return code


@router.get(
    "/",
    response_model=schemas.VerificationCode,
)
def get_verification_code_by_email(
    email: Annotated[str, Query(...)],
    db: Session = Depends(get_db),
    _: Admin = Depends(require_admin),
):
    """Get a verification code by email."""
    return crud.get_verification_code_by_email(db, email)


@router.get(
    "/{verification_code_id}",
    response_model=schemas.VerificationCode,
)
def get_verification_code(
    verification_code_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    _: Admin = Depends(require_admin),
):
    """Get a verification code by id."""
    return crud.get_verification_code_by_id(db, verification_code_id)


@router.put(
    "/verify",
    response_model=schemas.VerificationCode,
)
def verify_email_with_verification_code(
    verification_code: str = Query(min_length=6, max_length=6),
    email: str = Query(...),
    db: Session = Depends(get_db),
):
    """Update a verification code."""
    return crud.verify_email_with_code(db, email, verification_code)
