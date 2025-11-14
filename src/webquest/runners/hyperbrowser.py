import asyncio
from typing import TypeVar, override

from hyperbrowser import AsyncHyperbrowser
from playwright.async_api import async_playwright
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from webquest.base import BaseRunner, BaseScraper

TRequest = TypeVar("TRequest", bound=BaseModel)
TCollection = TypeVar("TCollection")
TResponse = TypeVar("TResponse", bound=BaseModel)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    hyperbrowser_api_key: str = Field(default=...)


class Runner(BaseRunner):
    def __init__(
        self,
        settings: Settings | None = None,
        hyperbrowser_client: AsyncHyperbrowser | None = None,
    ):
        self._settings = settings or Settings()
        self._hyperbrowser_client = hyperbrowser_client or AsyncHyperbrowser(
            api_key=self._settings.hyperbrowser_api_key,
        )

    @override
    async def run(
        self,
        scraper: BaseScraper[TRequest, TCollection, TResponse],
        requests: list[TRequest],
    ) -> list[TResponse]:
        session = await self._hyperbrowser_client.sessions.create()
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(session.ws_endpoint)
            context = browser.contexts[0]
            collections = await asyncio.gather(
                *[scraper.collect(context, request) for request in requests]
            )
        await self._hyperbrowser_client.sessions.stop(session.id)

        responses = await asyncio.gather(
            *[scraper.parse(collection) for collection in collections]
        )
        return responses
