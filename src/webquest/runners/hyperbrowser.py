import asyncio
from typing import TypeVar

from hyperbrowser import AsyncHyperbrowser
from playwright.async_api import async_playwright
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from webquest.base_scraper import BaseScraper

TRequest = TypeVar("TRequest", bound=BaseModel)
TRaw = TypeVar("TRaw")
TResponse = TypeVar("TResponse", bound=BaseModel)


class HyperbrowserSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    hyperbrowser_api_key: str | None = None


class Hyperbrowser:
    def __init__(
        self,
        settings: HyperbrowserSettings | None = None,
        hyperbrowser_client: AsyncHyperbrowser | None = None,
    ):
        self._settings = settings or HyperbrowserSettings()
        self._hyperbrowser_client = hyperbrowser_client or AsyncHyperbrowser(
            api_key=self._settings.hyperbrowser_api_key,
        )

    async def run_multiple(
        self,
        scraper: BaseScraper[TRequest, TRaw, TResponse],
        requests: list[TRequest],
    ) -> list[TResponse]:
        session = await self._hyperbrowser_client.sessions.create()
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(session.ws_endpoint)
            context = browser.contexts[0]
            raw_items = await asyncio.gather(
                *[scraper.fetch(context, request) for request in requests]
            )
        await self._hyperbrowser_client.sessions.stop(session.id)

        responses = await asyncio.gather(
            *[scraper.parse(raw_item) for raw_item in raw_items]
        )
        return responses

    async def run(
        self,
        scraper: BaseScraper[TRequest, TRaw, TResponse],
        request: TRequest,
    ) -> TResponse:
        responses = await self.run_multiple(scraper, [request])
        return responses[0]
