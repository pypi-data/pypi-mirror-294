"""
Validations for the subscription_utils app.
"""
from sqlalchemy.orm import Session

from . import crud, schemas, exceptions

def validate_user_is_stripe_client(db: Session, user_id: int) -> None:
    """
    Validates if the user is a client.
    """
    subscription = crud.get_subscription_by_user_id(db, user_id)
    if subscription.provider != schemas.SubscriptionProviderEnum.STRIPE or \
            subscription.status == schemas.SubscriptionStatusEnum.PENDING:
        raise exceptions.SubscriptionNotFound()
