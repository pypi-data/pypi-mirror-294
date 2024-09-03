"""This module defines the endpoints for the tickets API."""

from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from database import get_db
from user_entities.users import crud as user_crud, schemas as user_schemas
from user_entities.admin import schemas as admin_schemas
from raffles import schemas as raffle_schemas
from auth.middlewares import require_admin, require_user
from . import crud, schemas

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)


# TODO: la creación de tickets debe ser automática
# actualmente utilizado por workers
@router.post("/", response_model=schemas.Ticket)
def create_ticket(
    ticket: schemas.TicketCreate,
    db: Session = Depends(get_db),
):
    """Create a new ticket."""
    user_crud.get_user_by_id(db, ticket.user_id)
    return crud.create_ticket(db=db, ticket=ticket)


# TODO: borrar este endpoint
@router.get("/", response_model=list[schemas.Ticket])
def read_tickets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all tickets."""
    tickets = crud.get_tickets(db, skip=skip, limit=limit)
    return tickets


@router.get("/user", response_model=list[schemas.Ticket])
def read_user_tickets(
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(require_user),
):
    """Get all tickets for a user."""
    tickets = crud.get_user_tickets(db, user_id=current_user.id)
    return tickets


@router.get("/raffle", response_model=list[schemas.Ticket])
def read_raffle_tickets(
    raffle_id: Annotated[int, Query(ge=1)],
    db: Session = Depends(get_db),
    _: admin_schemas.Admin = Depends(require_admin),
):
    """Get all tickets for a raffle."""
    tickets = crud.get_raffle_tickets(db, raffle_id=raffle_id)
    return tickets


@router.get("/{ticket_id}", response_model=schemas.Ticket)
def read_ticket(
    ticket_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(require_user),
):
    """Get a ticket by ID."""
    db_ticket = crud.get_ticket_by_id_and_user_id(
        db, ticket_id=ticket_id, user_id=current_user.id
    )
    return db_ticket


@router.put("/unassign/{ticket_id}", response_model=schemas.Ticket)
def unassign_ticket(
    ticket_id: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(require_user),
):
    """Unassign a ticket from a raffle."""
    ticket = crud.unassign_ticket(
        db, ticket_id=ticket_id, current_user_id=current_user.id
    )
    return ticket


@router.put("/assign/{ticket_id}", response_model=schemas.Ticket)
def assign_raffle_ticket(
    ticket_id: Annotated[int, Path(ge=1)],
    raffle: raffle_schemas.RaffleAssignment,
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(require_user),
):
    """Assign a ticket to a raffle."""
    ticket = crud.assign_raffle_ticket(
        db,
        ticket_id=ticket_id,
        raffle_id=raffle.raffle_id,
        current_user_id=current_user.id,
    )
    return ticket


@router.put("/reassign/{ticket_id}", response_model=schemas.Ticket)
def reassign_raffle_ticket(
    ticket_id: Annotated[int, Path(ge=1)],
    new_raffle: raffle_schemas.RaffleAssignment,
    db: Session = Depends(get_db),
    current_user: user_schemas.User = Depends(require_user),
):
    """Assign a ticket to a raffle."""
    ticket = crud.reassign_ticket(
        db,
        ticket_id=ticket_id,
        new_raffle_id=new_raffle.raffle_id,
        current_user_id=current_user.id,
    )
    return ticket
