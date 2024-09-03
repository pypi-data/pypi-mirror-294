""" This module contains the exceptions for all users. """

from fastapi import HTTPException, status
from pydantic import BaseModel


class EmailNotVerifiedError(HTTPException):
    """
    Exception raised when a user's email is not verified.
    """

    class EmailNotVerifiedErrorSchema(BaseModel):
        """
        Schema for the EmailNotVerifiedError exception.
        """

        detail: str = """
        Email not verified or code expired.
        Please get a new verification code."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.EmailNotVerifiedErrorSchema().detail,
        )
