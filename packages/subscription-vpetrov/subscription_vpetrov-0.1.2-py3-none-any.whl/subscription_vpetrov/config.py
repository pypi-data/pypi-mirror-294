"""
Configuration file for the subscription utils repository.
"""
from os import getenv
from functools import lru_cache
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    App settings class.
    """
    model_config: ConfigDict = ConfigDict(
        env_file=".env" if not getenv("DB_URL") else None, extra="allow"
    )
    db_url: str = "sqlite:///./subscription.db"\
        if not getenv("DB_URL") else getenv("DB_URL")
    db_echo: bool = False
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 3600
    db_pool_pre_ping: bool = True


@lru_cache
def get_settings() -> Settings:
    """
    Returns the app settings.
    """
    return Settings()
