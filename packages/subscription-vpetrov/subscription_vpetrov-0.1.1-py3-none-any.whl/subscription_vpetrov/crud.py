"""CRUD operations for payku subscriptions"""
from sqlalchemy.orm import Session

from . import models, exceptions


def get_subscription_by_id(
        db: Session, subscription_id: int) -> models.Subscription:
    """
    Returns a Subscription with selected id.
    """
    subscription_db = db.query(models.Subscription).filter(
        models.Subscription.id == subscription_id).one_or_none()
    if subscription_db is None:
        raise exceptions.SubscriptionNotFound()
    return subscription_db


def get_subscription_by_user_id(
        db: Session, user_id: int) -> models.Subscription:
    """
    Returns a Subscription with selected user_id.
    """
    subscription_db = db.query(models.Subscription).filter(
        models.Subscription.user_id == user_id).one_or_none()
    if subscription_db is None:
        raise exceptions.SubscriptionNotFound()
    return subscription_db


def approve_subscription(
        db: Session, subscription_id: int) -> models.Subscription:
    """
    Approves a Subscription.
    """
    db_subscription = get_subscription_by_id(db, subscription_id)
    db_subscription.approve()
    db.commit()
    return db_subscription


def delete_subscription_if_exists(
        db: Session, subscription_id: int) -> None:
    """
    Deletes a Subscription if exists.
    """
    subscription_db = db.query(models.Subscription).filter(
        models.Subscription.id == subscription_id).first()
    if subscription_db is None:
        return
    db.delete(subscription_db)
    db.commit()


def cancel_subscription(
        db: Session, subscription_id: int) -> models.Subscription:
    """
    Cancels a Subscription.
    """
    db_subscription = get_subscription_by_id(db, subscription_id)
    db_subscription.cancel()
    db.commit()
    return db_subscription


def suspend_subscription(
        db: Session, subscription_id: int) -> models.Subscription:
    """
    Suspends a Subscription
    """
    db_subscription = get_subscription_by_id(db, subscription_id)
    db_subscription.suspend()
    db.commit()
    return db_subscription
