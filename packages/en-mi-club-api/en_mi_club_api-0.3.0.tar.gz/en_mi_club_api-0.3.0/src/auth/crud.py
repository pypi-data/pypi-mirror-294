""" This module contains the functions for authenticating users and admins. """

from sqlalchemy.orm import Session
from user_entities.utils import hash_password, verify_password
from user_entities.users import crud as user_crud, exceptions as user_exceptions
from user_entities.admin import crud as admin_crud
from user_entities.commerce import (
    crud as commerce_crud,
    models as commerce_models,
)
from . import enums, schemas, utils, exceptions


def get_user_by_email_and_type(
    db: Session, email: str, account_type: enums.AccountType
):
    """
    Retrieve a user by email and account type.
    The user can be one of these two types:
    User, Admin
    """
    if account_type == enums.AccountType.USER:
        user = user_crud.get_user_by_email(db, email)
    elif account_type == enums.AccountType.ADMIN:
        user = admin_crud.get_admin_by_email(db, email)
    else:
        user = None

    if not user:
        raise user_exceptions.UserNotFoundError()

    return user


def generate_password_reset_token(
    db: Session, email: str, account_type: enums.AccountType
) -> str:
    """
    Generate a password reset token for a user.
    """
    get_user_by_email_and_type(db, email, account_type)

    token_data = schemas.RecoverPasswordTokenData(
        email=email, account_type=account_type
    )
    token = utils.create_password_reset_jwt(token_data)

    return token


def reset_password_with_token(db: Session, token: str, new_password: str):
    """
    Validate the token and reset the user's password.
    The user can be one of these two types:
    User, Admin
    """

    token_data = utils.verify_password_reset_jwt(token)

    email = token_data.email
    account_type = token_data.account_type

    user = get_user_by_email_and_type(db, email, account_type)

    hashed_password = hash_password(new_password)

    user.hashed_password = hashed_password
    db.commit()
    db.refresh(user)

    return {"message": "Password has been reset successfully."}


def change_commerce_account_password(
    db: Session,
    email: str,
    update_password_schema: schemas.ChangePasswordRequest,
) -> commerce_models.CommerceAccount:
    """
    Updates the password of a commerce account.
    """
    commerce_account = commerce_crud.get_commerce_account_by_email(db, email)

    if not verify_password(
        update_password_schema.old_password, commerce_account.hashed_password
    ):
        raise exceptions.InvalidCredentialsError()

    hashed_password = hash_password(update_password_schema.new_password)

    commerce_account.hashed_password = hashed_password
    db.commit()
    db.refresh(commerce_account)

    return commerce_account


def generate_new_password_commerce(db: Session, email: str) -> str:
    """
    Generate a random password for a commerce account, change it and return it to send it.
    """
    commerce_account = commerce_crud.get_commerce_account_by_email(db, email)
    password = utils.generate_random_password()
    hashed_password = hash_password(password)
    commerce_account.hashed_password = hashed_password
    db.commit()
    db.refresh(commerce_account)
    return password
