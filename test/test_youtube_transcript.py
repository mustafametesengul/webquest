import asyncio

from dotenv import load_dotenv

from webquest.runners import Hyperbrowser
from webquest.scrapers import YouTubeTranscript


async def main() -> None:
    load_dotenv()

    runner = Hyperbrowser()
    scraper = YouTubeTranscript()

    response = await runner.run(
        scraper,
        scraper.Request(video_id="5OyWJeZ6ZrE"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
