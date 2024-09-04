""" CRUD operations for In-Person Benefits """

from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime
from benefits import exceptions, utils
from user_entities.users import crud as user_crud
from commerces import crud as commerce_crud
from . import models, schemas


def get_in_person_benefit_by_id(db: Session, in_person_benefit_id: int):
    """Get an in-person benefit by ID."""
    in_person_benefit = (
        db.query(models.InPersonBenefit)
        .filter(models.InPersonBenefit.id == in_person_benefit_id)
        .one_or_none()
    )
    if in_person_benefit is None:
        raise exceptions.BenefitNotFoundError()
    return in_person_benefit


def get_in_person_benefits(db: Session, skip: int = 0, limit: int = 100):
    """Get all in-person benefits."""
    return db.query(models.InPersonBenefit).offset(skip).limit(limit).all()


def create_in_person_benefit(
    db: Session, in_person_benefit: schemas.CreateInPersonBenefit
):
    """Create a new in-person benefit."""
    commerce_crud.get_commerce_by_id(db, in_person_benefit.commerce_id)
    db_in_person_benefit = models.InPersonBenefit(
        **in_person_benefit.model_dump(exclude_none=True)
    )
    db.add(db_in_person_benefit)
    db.commit()
    db.refresh(db_in_person_benefit)
    return db_in_person_benefit


def delete_in_person_benefit(db: Session, in_person_benefit_id: int):
    """Delete an in-person benefit."""
    db_in_person_benefit = get_in_person_benefit_by_id(db, in_person_benefit_id)
    db.delete(db_in_person_benefit)
    db.commit()
    return db_in_person_benefit


# TODO: Implement validations (quantity of benefits obtained, etc.)
def assign_in_person_benefit_to_user(
    db: Session, user_id: int, in_person_benefit_id: int, commerce_id: int
) -> models.UserInPersonBenefitAssociation:
    """Assign an in person benefit to a user."""
    benefit = get_in_person_benefit_by_id(db, in_person_benefit_id)
    if commerce_id != benefit.commerce_id:
        raise exceptions.BenefitDoesntBelongToCommerceError()
    user_crud.get_user_by_id(db, user_id)
    utils.validate_if_user_can_get_benefit(
        db, user_id, in_person_benefit_id, is_online=False
    )

    user_benefit = models.UserInPersonBenefitAssociation(
        user_id=user_id, in_person_benefit_id=in_person_benefit_id
    )

    db.add(user_benefit)
    db.commit()
    db.refresh(user_benefit)

    return user_benefit


def get_in_person_benefits_by_user(db: Session, user_id: int):
    """Retrieve all in person benefits claimed by a user."""
    user_crud.get_user_by_id(db, user_id)
    return (
        db.query(models.UserInPersonBenefitAssociation)
        .filter(models.UserInPersonBenefitAssociation.user_id == user_id)
        .all()
    )


def count_in_person_benefits_obtained_by_user(
    db: Session, user_id: int, start_date: datetime, end_date: datetime
) -> int:
    """
    Count the number of in_person benefits a user has obtained between certain dates.
    """
    benefits_obtained = (
        db.query(func.count(models.UserInPersonBenefitAssociation.id))
        .filter(
            models.UserInPersonBenefitAssociation.user_id == user_id,
            models.UserInPersonBenefitAssociation.created_at >= start_date,
            models.UserInPersonBenefitAssociation.created_at < end_date,
        )
        .scalar()
    )

    return benefits_obtained


def count_in_person_benefit_by_user_and_benefit(
    db: Session,
    user_id: int,
    benefit_id: int,
    start_date: datetime,
    end_date: datetime,
) -> int:
    """
    Count the number of times a user has obtained a specific in-person benefit
    within a specified date range.
    """
    return (
        db.query(func.count(models.UserInPersonBenefitAssociation.id))
        .filter(
            models.UserInPersonBenefitAssociation.user_id == user_id,
            models.UserInPersonBenefitAssociation.in_person_benefit_id
            == benefit_id,
            models.UserInPersonBenefitAssociation.created_at >= start_date,
            models.UserInPersonBenefitAssociation.created_at < end_date,
        )
        .scalar()
    )
