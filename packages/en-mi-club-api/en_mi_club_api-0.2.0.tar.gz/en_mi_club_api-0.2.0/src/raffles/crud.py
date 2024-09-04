""" CRUD operations for Raffles """

from sqlalchemy.orm import Session
from . import models, schemas, exceptions


def get_raffle_by_id(db: Session, raffle_id: int) -> models.Raffle:
    """Get a raffle by ID."""
    raffle = (
        db.query(models.Raffle)
        .filter(models.Raffle.id == raffle_id)
        .one_or_none()
    )
    if raffle is None:
        raise exceptions.RaffleNotFoundError()
    return raffle


def get_raffles(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.Raffle]:
    """Get all raffles."""
    return db.query(models.Raffle).offset(skip).limit(limit).all()


def create_raffle(db: Session, raffle: schemas.RaffleCreate) -> models.Raffle:
    """Create a new raffle."""
    db_raffle = models.Raffle(**raffle.model_dump(exclude_none=True))
    db.add(db_raffle)
    db.commit()
    db.refresh(db_raffle)
    return db_raffle


def delete_raffle(db: Session, raffle_id: int):
    """Delete a raffle."""
    db_raffle = get_raffle_by_id(db, raffle_id)
    db.delete(db_raffle)
    db.commit()
    return db_raffle
