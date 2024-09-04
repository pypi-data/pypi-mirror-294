"""Enums for the payment requests module"""

from enum import Enum


class Bank(str, Enum):
    """Banks"""

    BANCO_ESTADO = "Banco Estado"
    BANCO_FALABELLA = "Banco Falabella"
    BANCO_ITAU = "Banco Itau"
    BANCO_SANTANDER = "Banco Santander"
    BANCO_BICE = "Banco BICE"
    BANCO_RIPLEY = "Banco Ripley"
    BANCO_BBVA = "BBVA"
    BANCO_DESARROLLO = "Banco del Desarrollo"
    COOPEUCH_DALE = "Coopeuch/Dale"
    LA_POLAR_PREPAGO = "La Polar Prepago"
    PREPAGO_LOS_HEROES = "Prepago Los Heroes"
    TENPO_PREPAGO = "Tenpo Prepago"
    TAPP_CAJA_LOS_ANDES = "TAPP Caja los Andes"
    GLOBAL66 = "Global66"
    COPEC_PAY = "Copec Pay"
    MERCADO_PAGO = "Mercado Pago"
    BANCO_SECURITY = "Banco Security"
    RABOBANK = "RaboBank"
    BANCO_CONSORCIO = "Banco Consorcio"
    BANCO_PARIS = "Banco Paris"
    BANCO_CHILE_EDWARDS = "Banco Chile/Edwards"
    BANCO_INTERNACIONAL = "Banco Internacional"
    BANCO_SCOTIABANK = "Banco Scotiabank"
    BANCO_BCI_MACH = "Banco BCI/MACH"
    BANCO_DO_BRASIL = "Banco do Brasil S.A"
    CORPBANCA = "Corpbanca"
    BANCO_HSBC = "Banco HSBC Bank"


class AccountType(str, Enum):
    """Account types"""

    CTA_CORRIENTE = "Cuenta Corriente"
    CTA_VISTA = "Cuenta Vista"
    CTA_AHORRO = "Cuenta Ahorro"
