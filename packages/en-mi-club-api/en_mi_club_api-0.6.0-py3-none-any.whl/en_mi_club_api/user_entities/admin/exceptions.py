""" Exceptions for the admin app. """

from fastapi import HTTPException, status
from pydantic import BaseModel


class DuplicateAdminError(HTTPException):
    """
    Exception raised when a admin with the same username already exists.
    """

    class DuplicateAdminErrorSchema(BaseModel):
        """
        Schema for the DuplicateAdminError exception.
        """

        detail: str = "A admin with the same username already exists."

    def __init__(self):
        schema_instance = self.DuplicateAdminErrorSchema()
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, detail=schema_instance.detail
        )


class AdminNotFoundError(HTTPException):
    """
    Exception raised when an admin is not found.
    """

    class AdminNotFoundErrorSchema(BaseModel):
        """
        Schema for the AdminNotFoundError exception.
        """

        detail: str = "Admin not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.AdminNotFoundErrorSchema().detail,
        )
