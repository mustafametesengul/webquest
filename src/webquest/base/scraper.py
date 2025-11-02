from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from playwright.async_api import BrowserContext
from pydantic import BaseModel

TRequest = TypeVar("TRequest", bound=BaseModel)
TCollection = TypeVar("TCollection")
TResult = TypeVar("TResult", bound=BaseModel)


class BaseScraper(ABC, Generic[TRequest, TCollection, TResult]):
    @abstractmethod
    async def collect(
        self, context: BrowserContext, request: TRequest
    ) -> TCollection: ...

    @abstractmethod
    async def parse(self, collection: TCollection) -> TResult: ...
