import asyncio

from dotenv import load_dotenv

from webquest.browsers import Hyperbrowser
from webquest.scrapers import YouTubeSearch


async def main() -> None:
    load_dotenv()

    scraper = YouTubeSearch(browser=Hyperbrowser())

    response = await scraper.run(
        scraper.request_model(query="H3 Podcast"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
