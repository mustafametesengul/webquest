import asyncio

from webquest.runners.hyperbrowser import Runner
from webquest.scrapers.youtube_transcript import Request, Scraper


async def main() -> None:
    runner = Runner()
    response = await runner.run(
        Scraper(),
        Request(video_id="5OyWJeZ6ZrE"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
