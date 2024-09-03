""" Exceptions for the subscriptions app. """

from fastapi import HTTPException, status
from pydantic import BaseModel


class SubscriptionNotFoundError(HTTPException):
    """
    Exception raised when a subscription is not found.
    """

    class SubscriptionNotFoundErrorSchema(BaseModel):
        """
        Schema for the SubscriptionNotFoundError exception.
        """

        detail: str = "Subscription not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.SubscriptionNotFoundErrorSchema().detail,
        )


class SubscriptionAlreadyExists(HTTPException):
    """
    Exception raised when a Subscription already exists.
    """

    class SubscriptionAlreadyExistsSchema(BaseModel):
        """
        Schema for the SubscriptionAlreadyExists model.
        """

        detail: str = "Subscription already exists."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=self.SubscriptionAlreadyExistsSchema().detail,
        )


class SubscriptionIsNotActive(HTTPException):
    """
    Exception raised when a Subscription is not active.
    """

    class SubscriptionIsNotActiveSchema(BaseModel):
        """
        Schema for the SubscriptionIsNotActive model.
        """

        detail: str = """
        You can't perform this action because the subscription is not active.
        """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=self.SubscriptionIsNotActiveSchema().detail,
        )
