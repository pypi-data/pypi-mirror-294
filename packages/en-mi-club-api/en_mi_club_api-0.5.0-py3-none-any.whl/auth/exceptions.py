""" Exceptions for the auth app."""

from fastapi import HTTPException, status
from pydantic import BaseModel


class InvalidCredentialsError(HTTPException):
    """
    Exception raised when the credentials provided are invalid.
    """

    class InvalidCredentialsErrorSchema(BaseModel):
        """
        Schema for the InvalidCredentialsError exception.
        """

        detail: str = (
            "Invalid credentials, email" " and/or password are incorrect."
        )

    def __init__(self):
        schema_instance = self.InvalidCredentialsErrorSchema()
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=schema_instance.detail,
        )


class InvalidTokenError(HTTPException):
    """
    Exception raised when the token provided is invalid.
    """

    class InvalidTokenErrorSchema(BaseModel):
        """
        Schema for the InvalidTokenError exception.
        """

        detail: str = "Invalid token."

    def __init__(self):
        schema_instance = self.InvalidTokenErrorSchema()
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=schema_instance.detail,
        )


class UnauthorizedException(HTTPException):
    """
    Exception raised when the user is not authorized to access a resource.
    """

    class UnauthorizedExceptionSchema(BaseModel):
        """
        Schema for the UnauthorizedException exception.
        """

        detail: str = "Unauthorized."

    def __init__(self):
        schema_instance = self.UnauthorizedExceptionSchema()
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=schema_instance.detail,
        )
