import asyncio

from webquest.runners.hyperbrowser import Runner
from webquest.scrapers.any_article import Request, Scraper


async def main() -> None:
    runner = Runner()
    response = await runner.run(
        Scraper(),
        Request(url="https://www.bbc.com/news/articles/cy5qgy93w9go"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
