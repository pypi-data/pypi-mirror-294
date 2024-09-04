""" Endpoints for the plans module. """

from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from database import get_db
from auth.middlewares import require_admin
from user_entities.admin.schemas import Admin as AdminSchema
from . import crud, schemas

router = APIRouter(
    prefix="/plans",
    tags=["plans"],
)


@router.post(
    "/",
    response_model=schemas.Plan,
)
def create_plan(
    plan: schemas.PlanCreate,
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Create a new plan."""
    return crud.create_plan(db=db, plan=plan)


@router.get("/", response_model=list[schemas.Plan])
def read_plans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all plans."""
    plans = crud.get_plans(db, skip=skip, limit=limit)
    return plans


@router.get("/{plan_id}", response_model=schemas.Plan)
def read_plan(
    plan_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
):
    """Get a plan by id."""
    db_plan = crud.get_plan_by_id(db, plan_id=plan_id)
    return db_plan


@router.delete("/{plan_id}", response_model=schemas.Plan)
def delete_plan(
    plan_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Delete a plan by id."""
    db_plan = crud.delete_plan(db, plan_id)
    return db_plan
