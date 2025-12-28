import asyncio

import pytest

from webquest.browsers import Hyperbrowser
from webquest.scrapers import DuckDuckGoSearch


@pytest.mark.integration
async def test_duckduckgo_search() -> None:
    scraper = DuckDuckGoSearch(browser=Hyperbrowser())

    responses = await scraper.run(
        scraper.request_model(query="TLDR News"),
        scraper.request_model(query="Lex Fridman"),
    )
    for response in responses:
        print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(test_duckduckgo_search())
