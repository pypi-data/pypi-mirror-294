""" Utils for the tickets module."""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import raffles.models as raffles_models
from subscriptions import (
    utils as subscriptions_utils,
    crud as subscriptions_crud,
)
from . import constants, exceptions, models


def validate_ticket_assignment_availability(
    db_ticket: models.Ticket,
    db_raffle: raffles_models.Raffle,
    user_id: int,
    db: Session,
):
    """Validate that the ticket can be assigned to the raffle."""
    subscription = subscriptions_crud.get_user_subscription(
        db=db, user_id=user_id
    )
    subscriptions_utils.validate_subscription_is_active(
        subscription=subscription
    )
    validate_raffle_ends_after_threshold(db_raffle)
    validate_ticket_is_not_expired(db_ticket)
    validate_raffle_ends_before_ticket_expiration(db_raffle, db_ticket)


def validate_ticket_unassignment_availability(
    db_ticket: models.Ticket, db_raffle: raffles_models.Raffle
):
    """Validate that the ticket can be unassigned from the raffle."""
    validate_raffle_ends_after_threshold(db_raffle)
    validate_ticket_is_not_expired(db_ticket)


def validate_raffle_ends_after_threshold(raffle: raffles_models.Raffle):
    """Validate that the raffle is not close to its end."""
    if (
        raffle.end_date
        and (raffle.end_date - timedelta(minutes=constants.MINUTES))
        < datetime.now()
    ):
        raise exceptions.TicketAssignmentError(
            detail="Cannot modify ticket close to raffle end time."
        )


def validate_ticket_is_not_expired(ticket: models.Ticket):
    """Validate that the ticket is not expired."""
    if ticket.expires_at < datetime.now():
        raise exceptions.TicketAssignmentError(
            detail="Ticket is expired and cannot be modified."
        )


def validate_raffle_ends_before_ticket_expiration(
    db_raffle: raffles_models.Raffle, db_ticket: models.Ticket
):
    """
    Validate that if the raffle has an end_date,
    it is equal or smaller than the ticket's expires_at date.
    """
    if db_raffle.end_date and db_ticket.expires_at < db_raffle.end_date:
        raise exceptions.TicketAssignmentError(
            detail="""Raffle's end date must be smaller
            than the ticket's expiration date."""
        )
