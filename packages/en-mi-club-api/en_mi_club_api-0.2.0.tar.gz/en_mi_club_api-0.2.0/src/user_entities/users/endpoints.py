"""This module contains the endpoints for the users API."""

from typing import Annotated
from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session
from database import get_db
from src.auth.middlewares import require_user, require_admin
from user_entities.admin import schemas as admin_schemas
from benefits.utils import validate_if_user_can_get_benefit
from . import crud, schemas, exceptions

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
    response_model=schemas.User,
    responses={
        409: {"model": exceptions.DuplicateUserError.DuplicateUserErrorSchema}
    },
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    db_user = crud.get_user_by_email_if_exists(db, email=user.email)
    if db_user:
        raise exceptions.DuplicateUserError()
    return crud.create_user(db=db, user=user)


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(require_user)):
    """Get the current user."""
    return current_user


@router.get("/validate-benefit", response_model=bool)
def can_user_get_benefit(
    benefit_id: int = Body(..., ge=1),
    is_online: bool = Body(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(require_user),
):
    """Validate if a user can get a benefit."""
    try:
        validate_if_user_can_get_benefit(
            db, current_user.id, benefit_id, is_online
        )
        return True
    except Exception:
        return False
    

# TODO: delete this, is for testing purposes
@router.get("/all-users", response_model=list[schemas.User])
def read_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all users."""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/", response_model=list[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: admin_schemas.Admin = Depends(require_admin),
):
    """Get all users."""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _: admin_schemas.Admin = Depends(require_admin),
):
    """Get a user by id."""
    db_user = crud.get_user_by_id(db, user_id=user_id)
    return db_user


@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _: admin_schemas.Admin = Depends(require_admin),
):
    """Delete a user by id."""
    db_user = crud.delete_user(db, user_id)
    return db_user
