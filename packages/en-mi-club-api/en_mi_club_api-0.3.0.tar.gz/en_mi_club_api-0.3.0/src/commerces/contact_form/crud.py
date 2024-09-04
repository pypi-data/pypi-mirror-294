""" Crud operations for the contact form. """

from sqlalchemy.orm import Session
from . import models, schemas, exceptions


def create_contact_form(
    db: Session, contact_form: schemas.ContactFormCreate
) -> models.ContactForm:
    """Create a new contact form."""
    db_contact_form = models.ContactForm(
        **contact_form.model_dump(exclude_none=True)
    )
    db.add(db_contact_form)
    db.commit()
    db.refresh(db_contact_form)
    return db_contact_form


def get_contact_form_by_id(
    db: Session, contact_form_id: int
) -> models.ContactForm:
    """Get a contact form by id."""
    contact_form = db.query(models.ContactForm).get(contact_form_id)
    if contact_form is None:
        raise exceptions.ContactMessageNotFoundError()
    return contact_form


def get_contact_forms(db: Session, skip: int = 0, limit: int = 100):
    """Get all contact forms."""
    return db.query(models.ContactForm).offset(skip).limit(limit).all()


def mark_contact_form_as_answered(db: Session, contact_form_id: int):
    """Mark a contact form as answered."""
    contact_form = get_contact_form_by_id(db, contact_form_id)
    contact_form.is_answered = True
    db.commit()
    return contact_form


def delete_contact_form(db: Session, contact_form_id: int):
    """Delete a contact form."""
    contact_form = get_contact_form_by_id(db, contact_form_id)
    db.delete(contact_form)
    db.commit()
    return contact_form


def get_unanswered_contact_forms(db: Session, skip: int = 0, limit: int = 100):
    """Get all unanswered contact forms."""
    return (
        db.query(models.ContactForm)
        .filter_by(is_answered=False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_contact_form_by_company(db: Session, company: str):
    """Get a contact form by company."""
    return db.query(models.ContactForm).filter_by(company=company).all()
