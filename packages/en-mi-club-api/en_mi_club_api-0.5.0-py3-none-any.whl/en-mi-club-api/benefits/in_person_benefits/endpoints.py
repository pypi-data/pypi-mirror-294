"""This module defines the endpoints for in person benefits."""

from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from database import get_db
from benefits.in_person_benefits import schemas
from auth.middlewares import (
    require_admin,
    require_user,
    require_commerce_account,
)
from user_entities.users import schemas as user_schemas
from user_entities.commerce import schemas as commerce_schemas
from . import crud

router = APIRouter(
    prefix="/in_person_benefits",
    tags=["in_person_benefits"],
)


@router.post(
    "/",
    response_model=schemas.InPersonBenefit,
)
def create_in_person_benefit(
    in_person_benefit: schemas.CreateInPersonBenefit,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Create a new in person benefit."""
    return crud.create_in_person_benefit(
        db=db, in_person_benefit=in_person_benefit
    )


@router.post(
    "/assign/{in_person_benefit_id}",
    response_model=schemas.UserInPersonBenefitAssociation,
)
def assign_in_person_benefit_to_user(
    in_person_benefit_id: Annotated[int, Path(ge=1)],
    user_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
    current_commerce_account: commerce_schemas.CommerceAccount = Depends(
        require_commerce_account
    ),
):
    """Assign an in person benefit to a user."""
    user_benefit = crud.assign_in_person_benefit_to_user(
        db, user_id, in_person_benefit_id, current_commerce_account.commerce_id
    )
    return user_benefit


@router.get(
    "/user", response_model=list[schemas.UserInPersonBenefitAssociation]
)
def get_user_in_person_benefits(
    current_user: user_schemas.User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Get all in person benefits a user has claimed."""
    user_benefits = crud.get_in_person_benefits_by_user(db, current_user.id)
    return user_benefits


@router.get("/", response_model=list[schemas.InPersonBenefit])
def read_in_person_benefits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all in person benefits."""
    in_person_benefits = crud.get_in_person_benefits(db, skip=skip, limit=limit)
    return in_person_benefits


@router.get("/{in_person_benefit_id}", response_model=schemas.InPersonBenefit)
def read_in_person_benefit(
    in_person_benefit_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
):
    """Get an in person benefit by id."""
    db_in_person_benefit = crud.get_in_person_benefit_by_id(
        db, in_person_benefit_id=in_person_benefit_id
    )
    return db_in_person_benefit


@router.delete(
    "/{in_person_benefit_id}", response_model=schemas.InPersonBenefit
)
def delete_in_person_benefit(
    in_person_benefit_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Delete an in person benefit by id."""
    db_in_person_benefit = crud.delete_in_person_benefit(
        db, in_person_benefit_id
    )
    return db_in_person_benefit
