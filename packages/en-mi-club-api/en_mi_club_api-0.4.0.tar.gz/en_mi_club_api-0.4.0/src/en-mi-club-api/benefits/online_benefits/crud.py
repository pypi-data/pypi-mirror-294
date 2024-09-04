""" CRUD operations for Online Benefits """

from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime
from benefits import exceptions, utils
from user_entities.users import crud as user_crud
from commerces import crud as commerce_crud
from . import models, schemas


def get_online_benefit_by_id(
    db: Session, online_benefit_id: int
) -> models.OnlineBenefit:
    """Get an online benefit by ID."""
    online_benefit = (
        db.query(models.OnlineBenefit)
        .filter(models.OnlineBenefit.id == online_benefit_id)
        .one_or_none()
    )
    if online_benefit is None:
        raise exceptions.BenefitNotFoundError()
    return online_benefit


def get_online_benefits(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.OnlineBenefit]:
    """Get all online benefits."""
    return db.query(models.OnlineBenefit).offset(skip).limit(limit).all()


def create_online_benefit(
    db: Session, online_benefit: schemas.CreateOnlineBenefit
) -> models.OnlineBenefit:
    """Create a new online benefit."""
    commerce_crud.get_commerce_by_id(db, online_benefit.commerce_id)
    db_online_benefit = models.OnlineBenefit(
        **online_benefit.model_dump(exclude_none=True)
    )
    db.add(db_online_benefit)
    db.commit()
    db.refresh(db_online_benefit)
    return db_online_benefit


def delete_online_benefit(db: Session, online_benefit_id: int):
    """Delete an online benefit."""
    db_online_benefit = get_online_benefit_by_id(db, online_benefit_id)
    db.delete(db_online_benefit)
    db.commit()
    return db_online_benefit


# TODO: Implement validations (quantity of benefits obtained, etc.)
def assign_online_benefit_to_user(
    db: Session, user_id: int, online_benefit_id: int
) -> models.UserOnlineBenefitAssociation:
    """Assign an online benefit to a user."""
    get_online_benefit_by_id(db, online_benefit_id)
    user_crud.get_user_by_id(db, user_id)
    utils.validate_if_user_can_get_benefit(
        db, user_id, online_benefit_id, is_online=True
    )

    # TODO: Implement code generation logic, the following is a placeholder
    code = "TEMP_CODE"

    # TODO: Implement expiration date logic, the following is a placeholder
    expiration_date = datetime.now()

    user_benefit = models.UserOnlineBenefitAssociation(
        user_id=user_id,
        online_benefit_id=online_benefit_id,
        expiration_date=expiration_date,
        code=code,
    )

    db.add(user_benefit)
    db.commit()
    db.refresh(user_benefit)

    return user_benefit


def get_online_benefits_by_user(db: Session, user_id: int):
    """Retrieve all benefits claimed by a user."""
    user_crud.get_user_by_id(db, user_id)
    return (
        db.query(models.UserOnlineBenefitAssociation)
        .filter(models.UserOnlineBenefitAssociation.user_id == user_id)
        .all()
    )


def count_online_benefits_obtained_by_user(
    db: Session, user_id: int, start_date: datetime, end_date: datetime
) -> int:
    """
    Count the number of online benefits a user has obtained between certain dates.
    """
    benefits_obtained = (
        db.query(func.count(models.UserOnlineBenefitAssociation.id))
        .filter(
            models.UserOnlineBenefitAssociation.user_id == user_id,
            models.UserOnlineBenefitAssociation.created_at >= start_date,
            models.UserOnlineBenefitAssociation.created_at < end_date,
        )
        .scalar()
    )

    return benefits_obtained


def count_online_benefit_by_user_and_benefit(
    db: Session,
    user_id: int,
    benefit_id: int,
    start_date: datetime,
    end_date: datetime,
) -> int:
    """
    Count the number of times a user has obtained a specific online benefit
    within a specified date range.
    """
    return (
        db.query(func.count(models.UserOnlineBenefitAssociation.id))
        .filter(
            models.UserOnlineBenefitAssociation.user_id == user_id,
            models.UserOnlineBenefitAssociation.online_benefit_id == benefit_id,
            models.UserOnlineBenefitAssociation.created_at >= start_date,
            models.UserOnlineBenefitAssociation.created_at < end_date,
        )
        .scalar()
    )
