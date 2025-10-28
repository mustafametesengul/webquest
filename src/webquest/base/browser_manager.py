from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncIterator

from playwright.async_api import BrowserContext, async_playwright


class BrowserManager(ABC):
    @abstractmethod
    @asynccontextmanager
    async def new_context(self) -> AsyncIterator[BrowserContext]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            try:
                yield context
            finally:
                await context.close()
                await browser.close()
