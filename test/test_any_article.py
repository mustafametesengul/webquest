import asyncio

from dotenv import load_dotenv

from webquest.browsers import Hyperbrowser
from webquest.scrapers import AnyArticle


async def main() -> None:
    load_dotenv()

    scraper = AnyArticle(browser=Hyperbrowser())

    response = await scraper.run(
        scraper.request_model(url="https://www.bbc.com/news/articles/cy5qgy93w9go"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
