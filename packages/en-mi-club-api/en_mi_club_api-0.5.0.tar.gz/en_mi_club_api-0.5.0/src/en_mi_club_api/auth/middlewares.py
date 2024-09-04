"""This module contains the authentication functions for admins and users."""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from user_entities.users import crud as user_crud, schemas as user_schemas
from user_entities.admin import crud as admin_crud, schemas as admin_schemas
from user_entities.commerce import (
    schemas as commerce_account_schemas,
    crud as commerce_account_crud,
)
from auth.utils import verify_token
from auth.exceptions import UnauthorizedException

admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/admin/token")
user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/user/token")
commerce_account_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/commerce_account/token"
)

# TODO: change User Not Found Exception to Unauthorized Exception


def require_user(
    token: str = Depends(user_oauth2_scheme), db: Session = Depends(get_db)
) -> user_schemas.User:
    """Retrieve the current user based on the token provided."""
    token_data = verify_token(token)
    user = user_crud.get_user_by_email(db, email=token_data.email)
    return user_schemas.User(**user.__dict__)


def require_admin(
    token: str = Depends(admin_oauth2_scheme), db: Session = Depends(get_db)
) -> admin_schemas.Admin:
    """Retrieve the current admin based on the token provided."""
    token_data = verify_token(token)
    admin = admin_crud.get_admin_by_email(db, email=token_data.email)
    return admin_schemas.Admin(**admin.__dict__)


def require_commerce_account(
    token: str = Depends(commerce_account_oauth2_scheme),
    db: Session = Depends(get_db),
) -> commerce_account_schemas.CommerceAccount:
    """
    Retrieve the current commerce account based on the token provided.
    """
    token_data = verify_token(token)
    commerce_account = commerce_account_crud.get_commerce_account_by_email(
        db, email=token_data.email
    )
    return commerce_account_schemas.CommerceAccount(**commerce_account.__dict__)


def require_main_commerce_account(
    token: str = Depends(commerce_account_oauth2_scheme),
    db: Session = Depends(get_db),
) -> commerce_account_schemas.CommerceAccount:
    """
    Retrieve the current commerce account based on the token provided.
    """
    token_data = verify_token(token)
    commerce_account = commerce_account_crud.get_commerce_account_by_email(
        db, email=token_data.email
    )
    if commerce_account.is_main:
        return commerce_account_schemas.CommerceAccount(
            **commerce_account.__dict__
        )
    else:
        raise UnauthorizedException()


def require_loggin(
    token: str = Depends(admin_oauth2_scheme) or Depends(user_oauth2_scheme),
    db: Session = Depends(get_db),
) -> None:
    """
    Retrieve the current user or admin based on the token provided.

    It can triggers the Admin not Found Exception 404 if does not find an admin.
    It can triggers the User not Found Exception 404 if does not find a user.
    """
    token_data = verify_token(token)

    if token_data.is_admin:
        admin_crud.get_admin_by_email(db, email=token_data.email)
    else:
        user_crud.get_user_by_email(db, email=token_data.email)
