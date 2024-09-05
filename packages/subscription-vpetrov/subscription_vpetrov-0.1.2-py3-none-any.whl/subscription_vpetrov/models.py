"""
Subscription Models
"""
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, Integer, Date, Enum
from sqlalchemy.orm import validates

from subscription_vpetrov.database import Base

from . import schemas


class Subscription(Base):
    """
    Subscription Model.
    """
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    new_billing_date = Column(Date, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    status = Column(Enum(schemas.SubscriptionStatusEnum), nullable=False)
    provider = Column(Enum(schemas.SubscriptionProviderEnum), nullable=True)
    plan = Column(Enum(schemas.SubscriptionPlanEnum), nullable=False)

    @validates("user_id")
    def validate_user_id(self, _, user_id):
        """
        Validates the user_id attribute.
        """
        if user_id < 1:
            raise ValueError("user_id must be greater than 0.")
        return user_id

    @validates("status")
    def validate_status(self, _, status):
        """
        Validates the status attribute.
        """
        if status not in schemas.SubscriptionStatusEnum:
            raise ValueError("Invalid status.")
        return status

    @validates("provider")
    def validate_provider(self, _, provider):
        """
        Validates the provider attribute.
        """
        if provider not in schemas.SubscriptionProviderEnum:
            raise ValueError("Invalid provider.")
        return provider

    @validates("plan")
    def validate_plan(self, _, plan):
        """
        Validates the plan attribute.
        """
        if plan not in schemas.SubscriptionPlanEnum:
            raise ValueError("Invalid plan.")
        return plan

    def approve(self) -> None:
        """
        Approves the subscription updating its status tu ACTIVE and
        its new billing date.
        """
        self.status = schemas.SubscriptionStatusEnum.ACTIVE
        self.new_billing_date = self.__calculate_new_billing_date()

    def __calculate_new_billing_date(self) -> date:
        """
        Returns the new billing date.
        """
        if self.subscription_plan == schemas.SubscriptionPlanEnum.MONTHLY:
            return date.today() + relativedelta(months=1)
        if self.subscription_plan == schemas.SubscriptionPlanEnum.ANNUALLY:
            return date.today() + relativedelta(years=1)
        return date.today() + relativedelta(weeks=1)

    def cancel(self) -> None:
        """
        Cancels the subscription updating its status to CANCELLED.
        """
        self.status = schemas.SubscriptionStatusEnum.CANCELLED

    def suspend(self) -> None:
        """
        Suspends the subscription updating its status to PAST_DUE.
        """
        self.status = schemas.SubscriptionStatusEnum.PAST_DUE
