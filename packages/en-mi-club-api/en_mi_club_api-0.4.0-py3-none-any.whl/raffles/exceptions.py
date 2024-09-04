""" Raffles exceptions """

from fastapi import HTTPException, status
from pydantic import BaseModel


class RaffleNotFoundError(HTTPException):
    """
    Exception raised when a raffle is not found.
    """

    class RaffleNotFoundErrorSchema(BaseModel):
        """
        Schema for the RaffleNotFoundError exception.
        """

        detail: str = "Raffle not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.RaffleNotFoundErrorSchema().detail,
        )
