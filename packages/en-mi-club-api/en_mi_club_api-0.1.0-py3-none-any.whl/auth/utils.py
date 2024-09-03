""" This module contains utility functions for the authentication system. """

import jwt
import secrets
import string
from sqlalchemy.orm import Session
from config import get_settings
from user_entities.users import crud as user_crud, schemas as user_schemas
from user_entities.admin import crud as admin_crud, schemas as admin_schemas
from user_entities.commerce import (
    schemas as commerce_account_schemas,
    crud as commerce_account_crud,
)
from user_entities.utils import verify_password
from auth.schemas import TokenData, Token, RecoverPasswordTokenData
from auth.exceptions import (
    InvalidTokenError,
    InvalidCredentialsError,
)

settings = get_settings()


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> user_schemas.User:
    """Authenticate a regular user and return the user object if valid."""
    user = user_crud.get_user_by_email(db, username)
    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError()
    return user_schemas.User(**user.__dict__)


def authenticate_admin(
    db: Session,
    username: str,
    password: str,
) -> admin_schemas.Admin:
    """Authenticate an admin user and return the admin object if valid."""
    admin = admin_crud.get_admin_by_email(db, username)
    if not verify_password(password, admin.hashed_password):
        raise InvalidCredentialsError()
    return admin_schemas.Admin(**admin.__dict__)


def authenticate_commerce_account(
    db: Session,
    username: str,
    password: str,
) -> commerce_account_schemas.CommerceAccount:
    """Authenticate a commerce account and return the object if valid."""
    commerce_account = commerce_account_crud.get_commerce_account_by_email(
        db, username
    )
    if not verify_password(password, commerce_account.hashed_password):
        raise InvalidCredentialsError()
    return commerce_account_schemas.CommerceAccount(**commerce_account.__dict__)


def create_token_response(token_data: TokenData) -> Token:
    """Create a token response for an authenticated user or admin."""
    access_token = create_access_token(token_data)
    return Token(access_token=access_token)


def verify_token(token: str) -> TokenData:
    """Verify the token and return the token data."""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email: str = payload.get("email")
        if email is None:
            raise InvalidTokenError
        token_data = TokenData(**payload)
    except jwt.ExpiredSignatureError as e:
        raise InvalidTokenError from e
    except jwt.PyJWTError:
        raise InvalidTokenError
    return token_data


def create_access_token(token_data: TokenData) -> str:
    """Create an access token."""
    to_encode = token_data.model_dump()
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def create_password_reset_jwt(token_data: RecoverPasswordTokenData) -> str:
    """Create a password reset token."""
    to_encode = token_data.model_dump()
    encoded_jwt = jwt.encode(
        to_encode,
        settings.recover_password_secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def verify_password_reset_jwt(token: str) -> RecoverPasswordTokenData:
    """Validate a password reset token."""
    try:
        payload = jwt.decode(
            token,
            settings.recover_password_secret_key,
            algorithms=[settings.algorithm],
        )
        token_data = RecoverPasswordTokenData(**payload)
        return token_data
    except jwt.ExpiredSignatureError as e:
        raise InvalidTokenError from e
    except jwt.PyJWTError:
        raise InvalidTokenError


# From ChatGPT
def generate_random_password():
    """Generate a random password.
    It must contain at least one lowercase letter, one uppercase letter,
    one digit, and one special character.
    """
    # Define character pools
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special = "@$!%*#?&+-_.;,"

    # Generate one character from each pool
    password = [
        secrets.choice(lower),
        secrets.choice(upper),
        secrets.choice(digits),
        secrets.choice(special),
    ]

    # Fill the rest of the password length with random characters
    all_characters = lower + upper + digits + special
    # Between 6 and 20 characters total
    password += [
        secrets.choice(all_characters)
        for _ in range(secrets.choice(range(2, 16)))
    ]

    # Shuffle to ensure randomness
    secrets.SystemRandom().shuffle(password)

    # Convert list to string
    password = "".join(password)

    return password
