""" Crud for verification_code """

from datetime import datetime
from sqlalchemy.orm import Session
from . import models, schemas, exceptions


def create_or_refresh_verification_code(
    db: Session, email: str
) -> models.VerificationCode:
    """
    Create a new verification code or refresh it if it exists based on the email.
    """
    db_verification_code = get_verification_code_by_email_if_exists(db, email)

    verification_code_data = schemas.VerificationCodeCreate(email=email)

    if db_verification_code:
        db_verification_code.code = verification_code_data.code
        db_verification_code.expires_at = verification_code_data.expires_at
    else:
        db_verification_code = models.VerificationCode(
            **verification_code_data.model_dump()
        )
        db.add(db_verification_code)

    db.commit()
    db.refresh(db_verification_code)

    return db_verification_code


def get_verification_code_by_id_if_exists(
    db: Session, verification_code_id: int
) -> models.VerificationCode | None:
    """Get a verification code by id."""
    verification_code = (
        db.query(models.VerificationCode)
        .filter(models.VerificationCode.id == verification_code_id)
        .one_or_none()
    )
    return verification_code


def get_verification_code_by_id(
    db: Session, verification_code_id: int
) -> models.VerificationCode:
    """Get a verification code by id."""
    verification_code = get_verification_code_by_id_if_exists(
        db, verification_code_id
    )
    if not verification_code:
        raise exceptions.VerificationCodeNotFoundError()
    return verification_code


def get_verification_code_by_email_if_exists(
    db: Session, email: str
) -> models.VerificationCode | None:
    """Get a verification code by email."""
    verification_code = (
        db.query(models.VerificationCode)
        .filter(models.VerificationCode.email == email)
        .one_or_none()
    )
    return verification_code


def get_verification_code_by_email(
    db: Session, email: str
) -> models.VerificationCode:
    """Get a verification code by email."""
    verification_code = get_verification_code_by_email_if_exists(db, email)
    if not verification_code:
        raise exceptions.VerificationCodeNotFoundError()
    return verification_code


def delete_verification_code_by_id(db: Session, verification_code_id: int):
    """Delete a verification code by id."""
    verification_code = get_verification_code_by_id(db, verification_code_id)
    db.delete(verification_code)
    db.commit()
    return verification_code


def delete_verification_code_by_email(db: Session, email: str):
    """Delete a verification code by email."""
    verification_code = get_verification_code_by_email(db, email)
    db.delete(verification_code)
    db.commit()
    return verification_code


def verify_email_with_code(db: Session, email: str, code: str):
    """Verificate a email with code."""
    verification_code = get_verification_code_by_email(db, email)
    if verification_code.expires_at < datetime.now():
        raise exceptions.VerificationCodeExpiredError()
    if verification_code.code != code:
        raise exceptions.VerificationCodeInvalidError()
    verification_code.is_validated = True
    db.commit()
    return verification_code
