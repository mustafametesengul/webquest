import asyncio

from webquest.runners import Hyperbrowser
from webquest.scrapers import YouTubeTranscript, YouTubeTranscriptRequest


async def main() -> None:
    runner = Hyperbrowser()
    scraper = YouTubeTranscript()
    response = await runner.run(
        scraper,
        YouTubeTranscriptRequest(video_id="5OyWJeZ6ZrE"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
