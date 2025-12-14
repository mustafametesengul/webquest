from pydantic_settings import BaseSettings, SettingsConfigDict


class GoogleNewsSearchSettings(BaseSettings):
    """
    Configuration settings for the Google News search scraper.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    result_limit: int = 10
    character_limit: int = 1000
