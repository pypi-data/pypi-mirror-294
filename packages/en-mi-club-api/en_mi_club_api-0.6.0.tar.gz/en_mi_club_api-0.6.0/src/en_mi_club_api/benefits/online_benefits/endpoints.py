""" Endpoint for online benefits. """

from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from database import get_db
from benefits.online_benefits import schemas
from auth.middlewares import require_admin, require_user
from user_entities.users import schemas as user_schemas
from . import crud

router = APIRouter(
    prefix="/online_benefits",
    tags=["online_benefits"],
)


@router.post(
    "/",
    response_model=schemas.OnlineBenefit,
)
def create_online_benefit(
    online_benefit: schemas.CreateOnlineBenefit,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Create a new online benefit."""
    return crud.create_online_benefit(db=db, online_benefit=online_benefit)


@router.post(
    "/assign/{online_benefit_id}",
    response_model=schemas.UserOnlineBenefitAssociation,
)
def assign_online_benefit_to_user(
    online_benefit_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(require_user),
):
    """Assign an online benefit to a user."""
    user_benefit = crud.assign_online_benefit_to_user(
        db, current_user.id, online_benefit_id
    )
    return user_benefit


@router.get("/user", response_model=list[schemas.UserOnlineBenefitAssociation])
def get_user_online_benefits(
    current_user: user_schemas.User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Get all online benefits a user has claimed."""
    user_benefits = crud.get_online_benefits_by_user(db, current_user.id)
    return user_benefits


@router.get("/", response_model=list[schemas.OnlineBenefit])
def read_online_benefits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all online_benefits."""
    online_benefits = crud.get_online_benefits(db, skip=skip, limit=limit)
    return online_benefits


@router.get("/{online_benefit_id}", response_model=schemas.OnlineBenefit)
def read_online_benefit(
    online_benefit_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
):
    """Get an online benefit by id."""
    db_online_benefit = crud.get_online_benefit_by_id(
        db, online_benefit_id=online_benefit_id
    )
    return db_online_benefit


@router.delete("/{online_benefit_id}", response_model=schemas.OnlineBenefit)
def delete_online_benefit(
    online_benefit_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Delete an online benefit by id."""
    db_online_benefit = crud.delete_online_benefit(db, online_benefit_id)
    return db_online_benefit
