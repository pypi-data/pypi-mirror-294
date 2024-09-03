""" Exceptions for verification_code app. """

from fastapi import HTTPException, status
from pydantic import BaseModel


class VerificationCodeNotFoundError(HTTPException):
    """
    Exception raised when a verification code is not found.
    """

    class VerificationCodeNotFoundErrorSchema(BaseModel):
        """
        Schema for the VerificationCodeNotFoundError exception.
        """

        detail: str = "Verification code not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.VerificationCodeNotFoundErrorSchema().detail,
        )


class VerificationCodeExpiredError(HTTPException):
    """
    Exception raised when a verification code is expired.
    """

    class VerificationCodeExpiredErrorSchema(BaseModel):
        """
        Schema for the VerificationCodeExpiredError exception.
        """

        detail: str = "Verification code expired."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.VerificationCodeExpiredErrorSchema().detail,
        )


class VerificationCodeInvalidError(HTTPException):
    """
    Exception raised when a verification code is invalid.
    """

    class VerificationCodeInvalidErrorSchema(BaseModel):
        """
        Schema for the VerificationCodeInvalidError exception.
        """

        detail: str = "Verification code invalid."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.VerificationCodeInvalidErrorSchema().detail,
        )
