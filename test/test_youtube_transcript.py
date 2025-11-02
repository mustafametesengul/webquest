import asyncio

from webquest.runners.hyperbrowser import Runner
from webquest.scrapers.youtube_transcript import Request, Scraper


async def main() -> None:
    runner = Runner()

    results = await runner.run(
        Scraper(),
        [
            Request(video_id="5OyWJeZ6ZrE"),
        ],
    )

    for result in results:
        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
