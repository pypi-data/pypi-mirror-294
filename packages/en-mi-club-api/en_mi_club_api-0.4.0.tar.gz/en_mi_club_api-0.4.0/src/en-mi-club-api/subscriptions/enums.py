""" Enums for subscriptions. """

from enum import Enum


class Status(str, Enum):
    """Status for the subscriptions"""

    ACTIVE = "Activa"
    PENDING = "Pendiente"
    PAST_DUE = "Vencida"
    CANCELLED = "Cancelada"
