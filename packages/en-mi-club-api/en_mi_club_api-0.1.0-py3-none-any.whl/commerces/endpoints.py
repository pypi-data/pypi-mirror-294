""" Endpoints for the commerce module. """

from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from database import get_db
from auth.middlewares import require_admin
from user_entities.admin.schemas import Admin as AdminSchema
from . import crud, schemas

router = APIRouter(
    prefix="/commerces",
    tags=["commerces"],
)


@router.post(
    "/",
    response_model=schemas.Commerce,
)
def create_commerce(
    commerce: schemas.CommerceCreate,
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Create a new commerce."""
    return crud.create_commerce(db=db, commerce=commerce)


@router.get(
    "/",
    response_model=list[schemas.Commerce],
)
def get_commerces(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _: AdminSchema = Depends(require_admin),
):
    """Get all commerces."""
    return crud.get_commerces(db=db, skip=skip, limit=limit)


@router.get(
    "/{commerce_id}",
    response_model=schemas.Commerce,
)
def get_commerce_by_id(
    commerce_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Get a commerce by id."""
    return crud.get_commerce_by_id(db=db, commerce_id=commerce_id)


@router.delete(
    "/{commerce_id}",
    response_model=schemas.Commerce,
)
def delete_commerce(
    commerce_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Delete a commerce by id."""
    return crud.delete_commerce(db=db, commerce_id=commerce_id)
