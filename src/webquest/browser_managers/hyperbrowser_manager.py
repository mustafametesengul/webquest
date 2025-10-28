from contextlib import asynccontextmanager
from typing import AsyncIterator, override

from hyperbrowser import AsyncHyperbrowser
from playwright.async_api import Browser, BrowserContext, Playwright, async_playwright
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from webquest.base import BrowserManager


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    hyperbrowser_api_key: str = Field(default=...)


class HyperbrowserManager(BrowserManager):
    def __init__(
        self,
        settings: Settings | None = None,
        hyperbrowser_client: AsyncHyperbrowser | None = None,
    ):
        self._settings = settings or Settings()
        self._hyperbrowser_client = hyperbrowser_client or AsyncHyperbrowser(
            api_key=self._settings.hyperbrowser_api_key,
        )
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None

    async def __aenter__(self) -> "HyperbrowserManager":
        session = await self._hyperbrowser_client.sessions.create()
        pcm = async_playwright()
        self._playwright = await pcm.start()
        self._browser = await self._playwright.chromium.connect_over_cdp(
            session.ws_endpoint,
        )
        return self

    async def __aexit__(self, *_) -> None:
        if self._playwright:
            await self._playwright.stop()

    @override
    @asynccontextmanager
    async def new_context(self) -> AsyncIterator[BrowserContext]:
        if self._browser is not None:
            # context = await self._browser.new_context()
            contexts = self._browser.contexts
            context = contexts[0] if contexts else await self._browser.new_context()
            yield context
            await context.close()
            return

        session = await self._hyperbrowser_client.sessions.create()
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(
                session.ws_endpoint,
            )
            contexts = browser.contexts
            context = contexts[0] if contexts else await browser.new_context()
            yield context
