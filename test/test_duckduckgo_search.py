import asyncio

from webquest.runners.hyperbrowser import Runner
from webquest.scrapers.duckduckgo_search import Request, Scraper


async def main() -> None:
    runner = Runner()

    results = await runner.run(
        Scraper(),
        [
            Request(query="H3 Podcast"),
            Request(query="Moist Critical Gaming"),
        ],
    )

    for result in results:
        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
