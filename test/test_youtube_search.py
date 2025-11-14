import asyncio

from webquest.runners import Hyperbrowser
from webquest.scrapers import YouTubeSearch, YouTubeSearchRequest


async def main() -> None:
    runner = Hyperbrowser()
    scraper = YouTubeSearch()
    responses = await runner.run_multiple(
        scraper,
        [
            YouTubeSearchRequest(query="H3 Podcast"),
            YouTubeSearchRequest(query="Moist Critical Gaming"),
        ],
    )
    for response in responses:
        print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
