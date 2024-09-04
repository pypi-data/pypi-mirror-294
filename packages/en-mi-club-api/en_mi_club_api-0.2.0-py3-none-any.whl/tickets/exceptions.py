""" This module contains the exceptions for the tickets app. """

from fastapi import HTTPException, status
from pydantic import BaseModel


class TicketNotFoundError(HTTPException):
    """
    Exception raised when a ticket is not found.
    """

    class TicketNotFoundErrorSchema(BaseModel):
        """
        Schema for the TicketNotFoundError exception.
        """

        detail: str = "Ticket not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.TicketNotFoundErrorSchema().detail,
        )


class TicketAssignmentError(HTTPException):
    """
    Exception raised when a ticket cannot be assigned or unassigned.
    """

    class TicketAssignmentErrorSchema(BaseModel):
        """
        Schema for the TicketAssignmentError exception.
        """

        detail: str

    def __init__(self, detail: str = "Ticket assignment error."):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=self.TicketAssignmentErrorSchema(detail=detail).detail,
        )
