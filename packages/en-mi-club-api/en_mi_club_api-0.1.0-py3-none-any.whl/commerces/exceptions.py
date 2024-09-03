""" Exceptions for the commerces module. """

from fastapi import HTTPException, status
from pydantic import BaseModel


class CommerceNotFoundError(HTTPException):
    """
    Exception raised when a commerce is not found.
    """

    class CommerceNotFoundErrorSchema(BaseModel):
        """
        Schema for the CommerceNotFoundError exception.
        """

        detail: str = "Commerce not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.CommerceNotFoundErrorSchema().detail,
        )


class DuplicateCommerceError(HTTPException):
    """
    Exception raised when a commerce with the same data already exists.
    """

    class DuplicateCommerceErrorSchema(BaseModel):
        """
        Schema for the DuplicateCommerceError exception.
        """

        detail: str = "A commerce with the same data already exists."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=self.DuplicateCommerceErrorSchema().detail,
        )
