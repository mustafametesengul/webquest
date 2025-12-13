from pydantic_settings import BaseSettings, SettingsConfigDict


class YouTubeSearchSettings(BaseSettings):
    """
    Configuration settings for the YouTube search scraper.

    Attributes:
        result_limit: The maximum number of results to return. Defaults to 10.
        character_limit: The maximum number of characters to parse. Defaults to 1000.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    result_limit: int = 10
    character_limit: int = 1000
