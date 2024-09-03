""" This module contains the exceptions for the users app. """

from fastapi import HTTPException, status
from pydantic import BaseModel


class DuplicateUserError(HTTPException):
    """
    Exception raised when a user with the same data already exists.
    """

    class DuplicateUserErrorSchema(BaseModel):
        """
        Schema for the DuplicateUserError exception.
        """

        detail: str = "A user with the same data already exists."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=self.DuplicateUserErrorSchema().detail,
        )


class UserNotFoundError(HTTPException):
    """
    Exception raised when a user is not found.
    """

    class UserNotFoundErrorSchema(BaseModel):
        """
        Schema for the UserNotFoundError exception.
        """

        detail: str = "User not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.UserNotFoundErrorSchema().detail,
        )


class PromoCodeDoesntExistError(HTTPException):
    """
    Exception raised when a promo code is not found.
    """

    class PromoCodeDoesntExistErrorSchema(BaseModel):
        """
        Schema for the PromoCodeDoesntExistError exception.
        """

        detail: str = "Promo code doesn't exist."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.PromoCodeDoesntExistErrorSchema().detail,
        )
