""" Crud operations for plans. """

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, exceptions


def create_plan(db: Session, plan: schemas.PlanCreate) -> models.Plan:
    """Create a new plan."""
    db_plan = models.Plan(**plan.model_dump(exclude_none=True))
    db.add(db_plan)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise exceptions.DuplicatePlanError from e
    db.refresh(db_plan)
    return db_plan


def get_plan_by_id_if_exists(db: Session, plan_id: int) -> models.Plan | None:
    """Get a plan by ID."""
    plan = db.query(models.Plan).filter(models.Plan.id == plan_id).one_or_none()
    return plan


def get_plan_by_id(db: Session, plan_id: int) -> models.Plan:
    """Get a plan by ID."""
    plan = get_plan_by_id_if_exists(db, plan_id)
    if plan is None:
        raise exceptions.PlanNotFoundError()
    return plan


def get_plans(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.Plan]:
    """Get all plans."""
    return db.query(models.Plan).offset(skip).limit(limit).all()


def delete_plan(db: Session, plan_id: int):
    """Delete a plan."""
    db_plan = get_plan_by_id(db, plan_id)
    db.delete(db_plan)
    db.commit()
    return db_plan
