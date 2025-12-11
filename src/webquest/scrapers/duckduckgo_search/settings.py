from pydantic_settings import BaseSettings, SettingsConfigDict


class DuckDuckGoSearchSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    result_limit: int = 10
    character_limit: int = 1000
