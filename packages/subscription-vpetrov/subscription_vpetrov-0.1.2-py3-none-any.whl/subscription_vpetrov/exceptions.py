"""
Exceptions for the subscription utils lib.
"""
from fastapi import HTTPException, status
from pydantic import BaseModel


class SubscriptionNotFound(HTTPException):
    """
    Exception raised when a Subscription is not found.
    """

    class SubscriptionNotFoundSchema(BaseModel):
        """
        Schema for the SubscriptionNotFound model.
        """
        detail: str = "Subscription not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.SubscriptionNotFoundSchema().detail
        )
