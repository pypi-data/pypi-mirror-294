""" Exceptions for the wallet module. """

from fastapi import HTTPException, status
from pydantic import BaseModel


class WalletNotFoundError(HTTPException):
    """
    Exception raised when a wallet is not found.
    """

    class WalletNotFoundErrorSchema(BaseModel):
        """
        Schema for the WalletNotFoundError exception.
        """

        detail: str = "Wallet not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.WalletNotFoundErrorSchema().detail,
        )
