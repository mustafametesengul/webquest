from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AnyArticleSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    character_limit: int = 5000
    parser_model: str = "gpt-5-mini"
    openai_api_key: SecretStr | None = None
