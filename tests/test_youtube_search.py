import asyncio

import pytest

from webquest.browsers import Hyperbrowser
from webquest.scrapers import YouTubeSearch


@pytest.mark.integration
async def test_youtube_search() -> None:
    scraper = YouTubeSearch(browser=Hyperbrowser())

    response = await scraper.run(
        scraper.request_model(query="TLDR News"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(test_youtube_search())
