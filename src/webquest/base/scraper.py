from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from playwright.async_api import BrowserContext
from pydantic import BaseModel

from webquest.base.browser_manager import BrowserManager

TRequest = TypeVar("TRequest", bound=BaseModel)
TResult = TypeVar("TResult", bound=BaseModel)


class Scraper(ABC, Generic[TRequest, TResult]):
    def __init__(self, browser_manager: BrowserManager):
        self._browser_manager = browser_manager

    @abstractmethod
    async def scrape(self, context: BrowserContext, request: TRequest) -> TResult: ...

    async def run(self, request: TRequest) -> TResult:
        async with self._browser_manager.new_context() as context:
            return await self.scrape(context, request)
