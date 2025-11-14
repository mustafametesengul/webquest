import asyncio

from webquest.runners import Hyperbrowser
from webquest.scrapers import AnyArticle, AnyArticleRequest


async def main() -> None:
    runner = Hyperbrowser()
    scraper = AnyArticle()
    response = await runner.run(
        scraper,
        AnyArticleRequest(url="https://www.bbc.com/news/articles/cy5qgy93w9go"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
