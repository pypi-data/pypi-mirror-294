""" This module contains the endpoints for the authentication system. """

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from notifications.mailer.ses_service_functions import (
    send_forgot_password_mail,
    send_password_to_commerces,
)
from user_entities.commerce import schemas as commerce_schemas
from database import get_db
from . import schemas, utils, enums, crud

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/user/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Get an access token for a user and login"""
    user = utils.authenticate_user(db, form_data.username, form_data.password)
    token_data = schemas.TokenData(email=user.email, is_admin=False)
    return utils.create_token_response(token_data)


@router.post("/admin/token", response_model=schemas.Token)
def login_for_admin_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Get an access token for an admin and login"""
    admin = utils.authenticate_admin(db, form_data.username, form_data.password)
    token_data = schemas.TokenData(email=admin.email, is_admin=True)
    return utils.create_token_response(token_data)


@router.post("/commerce_account/token", response_model=schemas.Token)
def login_for_commerce_account_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Get an access token for commerce account and login"""
    commerce_account = utils.authenticate_commerce_account(
        db, form_data.username, form_data.password
    )
    token_data = schemas.TokenData(email=commerce_account.email, is_admin=False)
    return utils.create_token_response(token_data)


@router.post("/recover-password-users/")
def request_password_reset(
    email: str = Query(...),
    account_type: enums.AccountType = Query(...),
    db: Session = Depends(get_db),
):
    """Request a password recover for a user or admin
    and send the link with the token to the user's email."""
    token = crud.generate_password_reset_token(db, email, account_type)

    # TODO: Remove this print statement, it's only for testing purposes
    print(token)

    send_forgot_password_mail(email, token)

    return {"message": "Password reset email sent."}


@router.post("/reset-password-users/")
def reset_password(
    request: schemas.ResetPasswordRequest,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    """
    Endpoint to change the user's password using a JWT token.
    """
    return crud.reset_password_with_token(db, token, request.new_password)


@router.post("/recover-password-commerces/")
def recover_password_commerces(
    email: str = Query(...),
    db: Session = Depends(get_db),
):
    """
    Endpoint to recover the password for a commerce.
    It makes a new password, changes it and sends it by email.
    """
    password = crud.generate_new_password_commerce(db, email)
    # TODO: Remove this print statement, it's only for testing purposes
    print(password)
    send_password_to_commerces(email, password)
    return {"message": "Password sent to commerce."}


@router.post(
    "/change-password-commerces/",
    response_model=commerce_schemas.CommerceAccount,
)
def change_password_commerces(
    request: schemas.ChangePasswordRequest,
    email: str = Query(...),
    db: Session = Depends(get_db),
):
    """
    Endpoint to change the password for a commerce.
    """
    return crud.change_commerce_account_password(db, email, request)
