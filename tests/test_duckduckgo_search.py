import asyncio

from webquest.browsers import Hyperbrowser
from webquest.scrapers import DuckDuckGoSearch


async def main() -> None:
    scraper = DuckDuckGoSearch(browser=Hyperbrowser())

    responses = await scraper.run(
        scraper.request_model(query="H3 Podcast"),
        scraper.request_model(query="Moist Critical Gaming"),
    )
    for response in responses:
        print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
