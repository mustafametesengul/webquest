from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from webquest.base.scraper import BaseScraper

TRequest = TypeVar("TRequest", bound=BaseModel)
TCollection = TypeVar("TCollection")
TResult = TypeVar("TResult", bound=BaseModel)


class BaseRunner(ABC):
    @abstractmethod
    async def run(
        self,
        scraper: BaseScraper[TRequest, TCollection, TResult],
        requests: list[TRequest],
    ) -> list[TResult]: ...

    async def run_single(
        self,
        scraper: BaseScraper[TRequest, TCollection, TResult],
        request: TRequest,
    ) -> TResult:
        results = await self.run(scraper, [request])
        return results[0]
