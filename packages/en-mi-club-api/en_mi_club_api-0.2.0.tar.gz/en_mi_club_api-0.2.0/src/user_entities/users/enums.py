""" Enums for the users module, for the model and the schema. """

from enum import Enum


class Gender(str, Enum):
    """Genders"""

    FEMENINE = "Femenino"
    MASCULINE = "Masculino"
    PREFERS_NOT_TO_SAY = "Prefiero no decir"
