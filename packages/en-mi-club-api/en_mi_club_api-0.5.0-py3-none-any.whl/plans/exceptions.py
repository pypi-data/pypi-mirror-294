""" Exceptions for the plans module. """

from fastapi import HTTPException, status
from pydantic import BaseModel


class DuplicatePlanError(HTTPException):
    """
    Exception raised when a plan with the same data already exists.
    """

    class DuplicatePlanErrorSchema(BaseModel):
        """
        Schema for the DuplicatePlanError exception.
        """

        detail: str = "A plan with the same data already exists."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=self.DuplicatePlanErrorSchema().detail,
        )


class PlanNotFoundError(HTTPException):
    """
    Exception raised when a plan is not found.
    """

    class PlanNotFoundErrorSchema(BaseModel):
        """
        Schema for the PlanNotFoundError exception.
        """

        detail: str = "Plan not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.PlanNotFoundErrorSchema().detail,
        )
