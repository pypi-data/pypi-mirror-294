"""This module contains the configuration variables for the application."""

import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    App settings class.
    """

    # Database settings
    db_url: str = os.getenv("SQLALCHEMY_DATABASE_URL")
    db_echo: bool = False
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 3600
    db_pool_pre_ping: bool = True

    # Auth settings
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    )
    recover_password_secret_key: str = os.getenv("RECOVER_PASSWORD_SECRET_KEY")

    # AWS SES mailer settings
    aws_region_name: str = "us-east-1"
    aws_access_key_id_ses: str = os.getenv("AWS_ACCESS_KEY_ID_SES")
    aws_secret_access_key_ses: str = os.getenv("AWS_SECRET_ACCESS_KEY_SES")

    # Frontend
    frontend_url: str = os.getenv("FRONTEND_URL")


@lru_cache
def get_settings() -> Settings:
    """
    Returns the app settings.
    """
    return Settings()
