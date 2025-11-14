import asyncio

from webquest.runners.hyperbrowser import Runner
from webquest.scrapers.duckduckgo_search import Request, Scraper


async def main() -> None:
    runner = Runner()
    responses = await runner.run_multiple(
        Scraper(),
        [
            Request(query="H3 Podcast"),
            Request(query="Moist Critical Gaming"),
        ],
    )
    for response in responses:
        print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
