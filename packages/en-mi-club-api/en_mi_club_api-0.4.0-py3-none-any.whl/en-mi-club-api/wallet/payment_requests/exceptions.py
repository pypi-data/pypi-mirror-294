""" Exceptions for the payment request module. """

from fastapi import HTTPException, status
from pydantic import BaseModel


class PaymentRequestNotFoundError(HTTPException):
    """
    Exception raised when a payment request is not found.
    """

    class PaymentRequestNotFoundErrorSchema(BaseModel):
        """
        Schema for the PaymentRequestNotFoundError exception.
        """

        detail: str = "Payment request not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.PaymentRequestNotFoundErrorSchema().detail,
        )


class InsufficientFundsError(HTTPException):
    """
    Exception raised when a user has insufficient funds in the wallet
    to make a payment request.
    """

    class InsufficientFundsErrorSchema(BaseModel):
        """
        Schema for the InsufficientFundsError exception.
        """

        detail: str = (
            "Wallet balance must be greater than zero to create a payment request."
        )

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=self.InsufficientFundsErrorSchema().detail,
        )
