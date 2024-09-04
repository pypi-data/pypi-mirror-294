"""Raffles endpoints."""

from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from database import get_db
from auth.middlewares import require_admin
from user_entities.admin.schemas import Admin as AdminSchema
from . import crud, schemas

router = APIRouter(
    prefix="/raffles",
    tags=["raffles"],
)


@router.post(
    "/",
    response_model=schemas.Raffle,
)
def create_raffle(
    raffle: schemas.RaffleCreate,
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Create a new raffle."""
    return crud.create_raffle(db=db, raffle=raffle)


@router.get("/", response_model=list[schemas.Raffle])
def read_raffles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all raffles."""
    raffles = crud.get_raffles(db, skip=skip, limit=limit)
    return raffles


@router.get("/{raffle_id}", response_model=schemas.Raffle)
def read_raffle(
    raffle_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
):
    """Get a raffle by id."""
    db_raffle = crud.get_raffle_by_id(db, raffle_id=raffle_id)
    return db_raffle


@router.delete("/{raffle_id}", response_model=schemas.Raffle)
def delete_raffle(
    raffle_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Delete a raffle by id."""
    db_raffle = crud.delete_raffle(db, raffle_id)
    return db_raffle
