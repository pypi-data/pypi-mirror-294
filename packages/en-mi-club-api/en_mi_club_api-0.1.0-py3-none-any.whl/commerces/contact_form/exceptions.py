""" Exceptions for the contact form module. """

from fastapi import HTTPException, status
from pydantic import BaseModel


class ContactMessageNotFoundError(HTTPException):
    """
    Exception raised when a contact message is not found.
    """

    class ContactMessageNotFoundErrorSchema(BaseModel):
        """
        Schema for the ContactMessageNotFoundError exception.
        """

        detail: str = "Contact message not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.ContactMessageNotFoundErrorSchema().detail,
        )
