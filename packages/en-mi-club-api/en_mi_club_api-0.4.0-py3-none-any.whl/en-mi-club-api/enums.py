""" Enums for the app, for models and the schemas. """

from enum import Enum


class DocumentType(str, Enum):
    """Document types"""

    RUT = "RUT"


class Country(str, Enum):
    """Countries"""

    CL = "Chile"


class Currency(str, Enum):
    """Currencies"""

    CLP = "CLP"
