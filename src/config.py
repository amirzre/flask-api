from secrets import token_urlsafe

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """
    Base configuration settings.

    This class provides configuration values that are used throughout the application.
    It includes settings such as base directory, CORS origins, and other environment-based values.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="", env_nested_delimiter="__", case_sensitive=True
    )


class Config(BaseConfig):
    """
    Main configuration settings for the Flask application.

    This class extends the `BaseConfig` and provides specific configuration values
    for the application, including database URLs, security settings,
    and other operational parameters.
    """

    HOST: str = "0.0.0.0"
    PORT: int = 5000
    DEBUG: bool = False

    SECRET_KEY: str = token_urlsafe(32)

    DATABASE_URL: str = "postgresql://postgres:postgresql@127.0.0.1:5432/db"
    DATABASE_TEST_URL: str = "postgresql://postgres:postgresql@127.0.0.1:5432/db-test"


config: Config = Config()
