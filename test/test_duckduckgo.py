import asyncio

import webquest.scrapers.duckduckgo as duckduckgo
from webquest.browser_managers.hyperbrowser_manager import HyperbrowserManager


async def main() -> None:
    browser_manager = HyperbrowserManager()
    scraper = duckduckgo.SearchScraper(browser_manager=browser_manager)
    request = duckduckgo.SearchRequest(query="Moist Critical")
    result = await scraper.run(request)
    print(result.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
