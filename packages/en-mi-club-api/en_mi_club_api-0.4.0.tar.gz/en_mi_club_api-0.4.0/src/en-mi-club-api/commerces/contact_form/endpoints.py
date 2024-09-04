""" Endpoints for the contact form module. """

from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from database import get_db
from auth.middlewares import require_admin
from user_entities.admin.schemas import Admin as AdminSchema
from . import crud, schemas

router = APIRouter(
    prefix="/contact_forms",
    tags=["contact_forms"],
)


@router.post(
    "/",
    response_model=schemas.ContactForm,
)
def create_contact_form(
    contact_form: schemas.ContactFormCreate,
    db: Session = Depends(get_db),
):
    """Create a new contact form."""
    return crud.create_contact_form(db=db, contact_form=contact_form)


@router.get(
    "/",
    response_model=list[schemas.ContactForm],
)
def get_contact_forms(
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
    skip: int = 0,
    limit: int = 100,
):
    """Get all contact forms."""
    return crud.get_contact_forms(db=db, skip=skip, limit=limit)


@router.get(
    "/unanswered",
    response_model=list[schemas.ContactForm],
)
def get_unanswered_contact_forms(
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
    skip: int = 0,
    limit: int = 100,
):
    """Get all unanswered contact forms."""
    return crud.get_unanswered_contact_forms(db=db, skip=skip, limit=limit)


@router.get(
    "/company",
    response_model=list[schemas.ContactForm],
)
def get_contact_form_by_company(
    company: str = Query(...),
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Get a contact form by company."""
    return crud.get_contact_form_by_company(db=db, company=company)


@router.get(
    "/{contact_form_id}",
    response_model=schemas.ContactForm,
)
def get_contact_form_by_id(
    contact_form_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Get a contact form by id."""
    return crud.get_contact_form_by_id(db=db, contact_form_id=contact_form_id)


@router.put(
    "/{contact_form_id}",
    response_model=schemas.ContactForm,
)
def mark_contact_form_as_answered(
    contact_form_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Mark a contact form as answered."""
    return crud.mark_contact_form_as_answered(
        db=db, contact_form_id=contact_form_id
    )


@router.delete(
    "/{contact_form_id}",
    response_model=schemas.ContactForm,
)
def delete_contact_form(
    contact_form_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    _: AdminSchema = Depends(require_admin),
):
    """Delete a contact form by id."""
    return crud.delete_contact_form(db=db, contact_form_id=contact_form_id)
