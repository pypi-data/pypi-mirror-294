"""CRUD operations for the tickets module."""

from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from raffles.crud import get_raffle_by_id
from user_entities.users.crud import get_user_by_id
from . import models, schemas, exceptions, utils


def get_ticket_by_id_and_user_id(
    db: Session, ticket_id: int, user_id: int
) -> models.Ticket:
    """Get a ticket by its ID ans the user it belongs to."""
    ticket = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.id == ticket_id,
            models.Ticket.user_id == user_id,
        )
        .one_or_none()
    )
    if ticket is None:
        raise exceptions.TicketNotFoundError()
    return ticket


def get_tickets(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Ticket]:
    """Get all tickets."""
    return db.query(models.Ticket).offset(skip).limit(limit).all()


def create_ticket(db: Session, ticket: schemas.TicketBase) -> models.Ticket:
    """Create a new ticket."""
    db_ticket = models.Ticket(**ticket.model_dump(exclude_none=True))
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def get_user_tickets(db: Session, user_id: int) -> List[models.Ticket]:
    """Get all active (not expired) tickets for a user."""
    get_user_by_id(db, user_id)
    return (
        db.query(models.Ticket)
        .filter(models.Ticket.user_id == user_id)
        .filter(models.Ticket.expires_at > datetime.now())
        .all()
    )


def get_raffle_tickets(db: Session, raffle_id: int) -> List[models.Ticket]:
    """Get all tickets for a raffle."""
    get_raffle_by_id(db, raffle_id)
    return (
        db.query(models.Ticket)
        .filter(models.Ticket.raffle_id == raffle_id)
        .all()
    )


def assign_raffle_ticket(
    db: Session, ticket_id: int, raffle_id: int, current_user_id: int
) -> models.Ticket:
    """Assign or reassign a ticket to a raffle."""
    db_ticket = get_ticket_by_id_and_user_id(db, ticket_id, current_user_id)
    db_raffle = get_raffle_by_id(db, raffle_id)

    utils.validate_ticket_assignment_availability(
        db_ticket, db_raffle, current_user_id, db
    )

    db_raffle.tickets.append(db_ticket)
    db.commit()
    db.refresh(db_raffle)
    return db_ticket


def unassign_ticket(
    db: Session, ticket_id: int, current_user_id: int
) -> models.Ticket:
    """Unassign a ticket from a raffle."""
    db_ticket = get_ticket_by_id_and_user_id(db, ticket_id, current_user_id)
    db_raffle = get_raffle_by_id(db, db_ticket.raffle_id)

    utils.validate_ticket_unassignment_availability(db_ticket, db_raffle)

    db_raffle.tickets.remove(db_ticket)
    db.commit()
    db.refresh(db_raffle)
    return db_ticket


def reassign_ticket(
    db: Session, ticket_id: int, new_raffle_id: int, current_user_id: int
) -> models.Ticket:
    """
    Removes the ticket from its original raffle and assigns it to the new one
    """
    db_ticket = get_ticket_by_id_and_user_id(db, ticket_id, current_user_id)
    db_current_raffle = get_raffle_by_id(db, db_ticket.raffle_id)
    db_new_raffle = get_raffle_by_id(db, new_raffle_id)

    utils.validate_ticket_unassignment_availability(
        db_ticket, db_current_raffle
    )
    utils.validate_ticket_assignment_availability(
        db_ticket, db_new_raffle, current_user_id, db
    )

    db_current_raffle.tickets.remove(db_ticket)
    db_new_raffle.tickets.append(db_ticket)

    db.commit()
    db.refresh(db_new_raffle)

    return db_ticket
