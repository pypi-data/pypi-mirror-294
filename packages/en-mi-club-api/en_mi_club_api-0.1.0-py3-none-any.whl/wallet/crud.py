""" CRUD operations for the wallet module. """

from sqlalchemy.orm import Session
from . import models, schemas, exceptions


def create_wallet(db: Session, wallet: schemas.WalletCreate) -> models.Wallet:
    """Create a new wallet for a user."""
    db_wallet = models.Wallet(**wallet.model_dump(exclude_none=True))
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet


def get_wallet_by_user_id_if_exists(db: Session, user_id: int) -> models.Wallet:
    """Get a wallet by user ID."""
    wallet = (
        db.query(models.Wallet)
        .filter(models.Wallet.user_id == user_id)
        .one_or_none()
    )
    return wallet


def get_wallet_by_user_id(db: Session, user_id: int) -> models.Wallet:
    """Get a wallet by user ID."""
    wallet = get_wallet_by_user_id_if_exists(db, user_id)
    if wallet is None:
        raise exceptions.WalletNotFoundError()
    return wallet


def get_wallets(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.Wallet]:
    """Get all wallets."""
    return db.query(models.Wallet).offset(skip).limit(limit).all()


def increase_wallet_balance_by_user_id(
    db: Session, user_id: int, amount: int
) -> models.Wallet:
    """Increase the balance of a wallet."""
    wallet = get_wallet_by_user_id(db, user_id)
    wallet.balance += amount
    db.commit()
    db.refresh(wallet)
    return wallet
