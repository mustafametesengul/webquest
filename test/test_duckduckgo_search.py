import asyncio

from webquest.runners import Hyperbrowser
from webquest.scrapers import DuckDuckGoSearch


async def main() -> None:
    runner = Hyperbrowser()
    scraper = DuckDuckGoSearch()
    responses = await runner.run_multiple(
        scraper,
        [
            scraper.Request(query="H3 Podcast"),
            scraper.Request(query="Moist Critical Gaming"),
        ],
    )
    for response in responses:
        print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
