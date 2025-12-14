import asyncio

from webquest.browsers import Hyperbrowser
from webquest.scrapers import YouTubeTranscript


async def main() -> None:
    scraper = YouTubeTranscript(browser=Hyperbrowser())

    response = await scraper.run(
        scraper.request_model(video_id="dQw4w9WgXcQ"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
