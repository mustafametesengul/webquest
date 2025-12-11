from pydantic_settings import BaseSettings, SettingsConfigDict


class YouTubeTranscriptSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    character_limit: int = 5000
