""" This module contains the exceptions for the benefits module """

from fastapi import HTTPException, status
from pydantic import BaseModel


class BenefitNotFoundError(HTTPException):
    """
    Exception raised when a benefit is not found.
    """

    class BenefitNotFoundErrorSchema(BaseModel):
        """
        Schema for the BenefitNotFoundError exception.
        """

        detail: str = "Benefit not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.BenefitNotFoundErrorSchema().detail,
        )


class BenefitLimitExceededError(HTTPException):
    """
    Exception raised when a user exceeds the limit of benefits for this period.
    """

    class BenefitLimitExceededErrorSchema(BaseModel):
        """
        Schema for the BenefitLimitExceededError exception.
        """

        detail: str = "User has reached the limit of benefits for this period."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=self.BenefitLimitExceededErrorSchema().detail,
        )


class BenefitDoesntBelongToCommerceError(HTTPException):
    """
    Exception raised when a benefit doesn't belong to the commerce.
    """

    class BenefitDoesntBelongToCommerceErrorSchema(BaseModel):
        """
        Schema for the BenefitDoesntBelongToCommerceError exception.
        """

        detail: str = "Benefit doesn't belong to the commerce."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=self.BenefitDoesntBelongToCommerceErrorSchema().detail,
        )
