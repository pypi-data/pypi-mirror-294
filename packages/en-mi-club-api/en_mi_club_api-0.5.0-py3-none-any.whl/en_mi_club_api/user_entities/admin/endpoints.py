"""Admin endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from src.auth.middlewares import require_admin
from . import crud, schemas, exceptions

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.post(
    "/",
    response_model=schemas.Admin,
    responses={
        409: {"model": exceptions.DuplicateAdminError.DuplicateAdminErrorSchema}
    },
)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    """Create a new admin."""
    db_admin = crud.get_admin_by_email_if_exists(db, email=admin.email)
    if db_admin:
        raise exceptions.DuplicateAdminError()
    return crud.create_admin(db=db, admin=admin)


@router.get("/me", response_model=schemas.Admin)
def read_admins_me(current_admin: schemas.Admin = Depends(require_admin)):
    """Get the current admin."""
    return current_admin


@router.get("/", response_model=list[schemas.Admin])
def read_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all admins."""
    admins = crud.get_admins(db, skip=skip, limit=limit)
    return admins
