""" CRUD operations for Commerce model """

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, exceptions


def create_commerce(
    db: Session, commerce: schemas.CommerceCreate
) -> models.Commerce:
    """Create a new commerce."""
    db_commerce = models.Commerce(**commerce.model_dump(exclude_none=True))
    db.add(db_commerce)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise exceptions.DuplicateCommerceError from e
    db.refresh(db_commerce)
    return db_commerce


def get_commerce_by_id(db: Session, commerce_id: int) -> models.Commerce:
    """Get a commerce by id."""
    commerce = db.query(models.Commerce).get(commerce_id)
    if commerce is None:
        raise exceptions.CommerceNotFoundError()
    return commerce


def get_commerces(db: Session, skip: int = 0, limit: int = 100):
    """Get all commerces."""
    return db.query(models.Commerce).offset(skip).limit(limit).all()


def delete_commerce(db: Session, commerce_id: int):
    """Delete a commerce by id."""
    commerce = get_commerce_by_id(db, commerce_id)
    db.delete(commerce)
    db.commit()
    return commerce
