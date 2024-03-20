import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

FIXED_SETTINGS = {
    "ACCESS_TOKEN_EXPIRE_MINUTES": 30,  # 30 minutes
    "REFRESH_TOKEN_EXPIRE_MINUTES": 60 * 24 * 7,  # 7 days
    "TOKEN_ALGORITHM": "HS256",
}


class Settings(BaseSettings):
    DB_URI: str
    ECHO_SQL: bool
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    TOKEN_ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / f"config/{os.environ['APP_CONFIG_FILE']}.env",
        case_sensitive=True,
    )


settings = Settings.model_validate(FIXED_SETTINGS)
