import asyncio

import pytest

from webquest.browsers import Hyperbrowser
from webquest.scrapers import AnyArticle


@pytest.mark.integration
async def test_any_article() -> None:
    scraper = AnyArticle(browser=Hyperbrowser())

    response = await scraper.run(
        scraper.request_model(url="https://www.bbc.com/news/articles/cy5qgy93w9go"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(test_any_article())
