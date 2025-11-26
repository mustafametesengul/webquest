import asyncio
from typing import TypeVar, override

from hyperbrowser import AsyncHyperbrowser
from playwright.async_api import async_playwright
from pydantic import BaseModel

from webquest.runners.base_runner import BaseRunner
from webquest.scrapers.base_scraper import BaseScraper

TRequest = TypeVar("TRequest", bound=BaseModel)
TRaw = TypeVar("TRaw")
TResponse = TypeVar("TResponse", bound=BaseModel)


class Hyperbrowser(BaseRunner):
    """Runner that uses Hyperbrowser to execute scrapers."""

    def __init__(
        self,
        client: AsyncHyperbrowser | None = None,
    ):
        if client is None:
            client = AsyncHyperbrowser()
        self._client = client

    @override
    async def run_multiple(
        self,
        scraper: BaseScraper[TRequest, TRaw, TResponse],
        requests: list[TRequest],
    ) -> list[TResponse]:
        session = await self._client.sessions.create()
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(session.ws_endpoint)
            context = browser.contexts[0]
            raw_items = await asyncio.gather(
                *[scraper.fetch(context, request) for request in requests]
            )
        await self._client.sessions.stop(session.id)

        responses = await asyncio.gather(
            *[scraper.parse(raw_item) for raw_item in raw_items]
        )
        return responses
