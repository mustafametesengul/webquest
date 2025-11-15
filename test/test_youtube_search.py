import asyncio

from webquest.runners import Hyperbrowser
from webquest.scrapers import YouTubeSearch, YouTubeSearchRequest


async def main() -> None:
    runner = Hyperbrowser()
    scraper = YouTubeSearch()
    response = await runner.run(
        scraper,
        YouTubeSearchRequest(query="H3 Podcast"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
