"""
Schemas for the subscription app
"""
from enum import Enum


class SubscriptionPlanEnum(str, Enum):
    """
    Enum for the SubscriptionPlan model.
    """
    WEEKLY = "Semanal"
    MONTHLY = "Mensual"
    ANNUALLY = "Anual"


class SubscriptionStatusEnum(str, Enum):
    """
    Enum for the SubscriptionStatus model.
    """
    ACTIVE = "Activa"
    PENDING = "Pendiente"
    PAST_DUE = "Vencida"
    CANCELLED = "Cancelada"


class SubscriptionProviderEnum(str, Enum):
    """
    Enum for the SubscriptionProvider model.
    """
    STRIPE = "Stripe"
    PAYKU = "Payku"
