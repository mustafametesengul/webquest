import asyncio

from webquest.browsers import Hyperbrowser
from webquest.scrapers import GoogleNewsSearch


async def main() -> None:
    scraper = GoogleNewsSearch(browser=Hyperbrowser())

    response = await scraper.run(
        scraper.request_model(query="Artificial Intelligence"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
