""" Endpoints for wallet module. """

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from database import get_db
from auth.middlewares import require_admin, require_user
from user_entities.users import schemas as user_schemas
from user_entities.admin import schemas as admin_schemas
from . import schemas, crud

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"],
)


@router.get("/", response_model=list[schemas.Wallet])
def get_wallets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: admin_schemas.Admin = Depends(require_admin),
):
    """Get all wallets."""
    return crud.get_wallets(db, skip=skip, limit=limit)


@router.get("/user", response_model=schemas.Wallet)
def get_wallet_by_user_id(
    current_user: user_schemas.User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Get current user's wallet."""
    return crud.get_wallet_by_user_id(db, current_user.id)


@router.get("/{wallet_id}", response_model=schemas.Wallet)
def get_wallet_by_id(
    wallet_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: admin_schemas.Admin = Depends(require_admin),
):
    """Get wallet by ID."""
    return crud.get_wallet_by_id(db, wallet_id)


@router.put("/", response_model=schemas.Wallet)
def update_wallet_balance_by_user_id(
    wallet: schemas.WalletUpdate,
    user_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
    _: admin_schemas.Admin = Depends(require_admin),
):
    """Increase the balance of a wallet."""
    return crud.increase_wallet_balance_by_user_id(db, user_id, wallet.amount)
