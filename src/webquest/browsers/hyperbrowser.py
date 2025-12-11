import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, override

from hyperbrowser import AsyncHyperbrowser
from playwright.async_api import BrowserContext, async_playwright
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from webquest.browsers.browser import Browser


class HyperbrowserSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    hyperbrowser_api_key: SecretStr | None = None
    max_concurrent_sessions: int = 5


class Hyperbrowser(Browser[HyperbrowserSettings]):
    """
    A Browser implementation that uses Hyperbrowser for remote browser sessions.

    This class manages the creation and cleanup of Hyperbrowser sessions and provides
    a Playwright BrowserContext connected to the remote session.
    """

    settings_model = HyperbrowserSettings

    def __init__(
        self,
        settings: HyperbrowserSettings | None = None,
        client: AsyncHyperbrowser | None = None,
    ):
        """
        Initialize the Hyperbrowser instance.

        Args:
            settings (HyperbrowserSettings | None): Optional settings for Hyperbrowser.
            client (AsyncHyperbrowser | None): An optional AsyncHyperbrowser client.
                If not provided, a new client will be created.
        """
        super().__init__(settings=settings)

        if client is None:
            api_key = (
                self._settings.hyperbrowser_api_key.get_secret_value()
                if self._settings.hyperbrowser_api_key
                else None
            )
            client = AsyncHyperbrowser(api_key=api_key)

        self._client = client

        self._semaphore = asyncio.Semaphore(self._settings.max_concurrent_sessions)

    @override
    @asynccontextmanager
    async def get_context(self) -> AsyncIterator[BrowserContext]:
        """
        Get a browser context from a new Hyperbrowser session.

        This method creates a new session, connects to it using Playwright, yields
        the context, and ensures the session is stopped afterwards.

        Yields:
            BrowserContext: The Playwright browser context connected to the Hyperbrowser session.
        """
        async with self._semaphore:
            session = await self._client.sessions.create()
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(session.ws_endpoint)
                context = browser.contexts[0]
                try:
                    yield context
                finally:
                    await self._client.sessions.stop(session.id)
