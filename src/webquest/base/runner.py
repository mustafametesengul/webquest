from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from webquest.base.scraper import BaseScraper

TRequest = TypeVar("TRequest", bound=BaseModel)
TCollection = TypeVar("TCollection")
TResponse = TypeVar("TResponse", bound=BaseModel)


class BaseRunner(ABC):
    @abstractmethod
    async def run(
        self,
        scraper: BaseScraper[TRequest, TCollection, TResponse],
        requests: list[TRequest],
    ) -> list[TResponse]: ...

    async def run_single(
        self,
        scraper: BaseScraper[TRequest, TCollection, TResponse],
        request: TRequest,
    ) -> TResponse:
        results = await self.run(scraper, [request])
        return results[0]
