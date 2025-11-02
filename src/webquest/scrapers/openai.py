from abc import ABC
from typing import Generic, Type, TypeVar, override

from bs4 import BeautifulSoup
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from webquest.base.scraper import BaseScraper

TRequest = TypeVar("TRequest", bound=BaseModel)
TResult = TypeVar("TResult", bound=BaseModel)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    openai_api_key: str = Field(default=...)


class OpenAIBaseScraper(
    Generic[TRequest, TResult],
    BaseScraper[TRequest, str, TResult],
    ABC,
):
    def __init__(
        self,
        result_type: Type[TResult],
        openai: AsyncOpenAI | None = None,
        settings: Settings | None = None,
        model: str = "gpt-5-mini",
        extra_input: str | None = None,
        character_limit: int = 20000,
    ) -> None:
        self._result_type = result_type
        if settings is None:
            settings = Settings()
        self._settings = settings
        if openai is None:
            openai = AsyncOpenAI(api_key=self._settings.openai_api_key)
        self._openai = openai
        self._model = model
        self._character_limit = character_limit

        self._input = "Parse the following web page and extract the main article."
        if extra_input is not None:
            self._input = f"{self._input}\n\n{extra_input}"
        self._input = f"{self._input}\n\nWeb page:\n\n"

    @override
    async def parse(self, collection: str) -> TResult:
        soup = BeautifulSoup(collection, "html.parser")
        text = soup.get_text(separator="\n", strip=True)

        if len(text) > self._character_limit:
            start = (len(text) - self._character_limit) // 2
            end = start + self._character_limit
            text = text[start:end]

        response = await self._openai.responses.parse(
            input=f"{self._input}{text}",
            text_format=self._result_type,
            model=self._model,
            reasoning={"effort": "minimal"},
        )
        if response.output_parsed is None:
            raise ValueError("Failed to parse the response into the desired format.")
        return response.output_parsed
