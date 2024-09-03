"""CRUD operations for the admin model."""

from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from user_entities.utils import hash_password
from user_entities.exceptions import EmailNotVerifiedError
from verification_code.crud import (
    get_verification_code_by_email,
    delete_verification_code_by_email,
)
from . import models, schemas, exceptions


def get_admin(db: Session, admin_id: int) -> models.Admin:
    """Get an admin by ID."""
    return (
        db.query(models.Admin).filter(models.Admin.id == admin_id).one_or_none()
    )


def get_admin_by_email_if_exists(
    db: Session, email: str
) -> models.Admin | None:
    """Get an admin by email."""
    return (
        db.query(models.Admin).filter(models.Admin.email == email).one_or_none()
    )


def get_admin_by_email(db: Session, email: str) -> models.Admin:
    """Get an admin by email."""
    admin = get_admin_by_email_if_exists(db, email)
    if admin is None:
        raise exceptions.AdminNotFoundError()
    return admin


def get_admins(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Admin]:
    """Get all admins."""
    return db.query(models.Admin).offset(skip).limit(limit).all()


def create_admin(db: Session, admin: schemas.AdminCreate) -> models.Admin:
    """Create a new admin."""
    code = get_verification_code_by_email(db, admin.email)
    if not code.is_validated or code.expires_at < datetime.now():
        raise EmailNotVerifiedError()
    hashed_password = hash_password(admin.password)
    db_admin = models.Admin(
        **admin.model_dump(exclude={"password"}),
        hashed_password=hashed_password
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    delete_verification_code_by_email(db, admin.email)
    return db_admin
