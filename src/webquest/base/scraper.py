import asyncio
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from playwright.async_api import BrowserContext
from pydantic import BaseModel

TRequest = TypeVar("TRequest", bound=BaseModel)
TCollection = TypeVar("TCollection")
TResponse = TypeVar("TResponse", bound=BaseModel)


class BaseScraper(ABC, Generic[TRequest, TCollection, TResponse]):
    @abstractmethod
    async def collect(
        self, context: BrowserContext, request: TRequest
    ) -> TCollection: ...

    @abstractmethod
    async def parse(self, collection: TCollection) -> TResponse: ...
