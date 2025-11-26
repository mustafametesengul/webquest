import asyncio

from dotenv import load_dotenv

from webquest.runners import Hyperbrowser
from webquest.scrapers import GoogleNewsSearch


async def main() -> None:
    load_dotenv()

    runner = Hyperbrowser()
    scraper = GoogleNewsSearch()

    response = await runner.run(
        scraper,
        scraper.Request(query="Artificial Intelligence"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
