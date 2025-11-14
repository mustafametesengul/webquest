from typing import override

from openai import AsyncOpenAI
from playwright.async_api import BrowserContext

from webquest.scrapers.any_article.schemas import Request, Response
from webquest.scrapers.openai import OpenAIBaseScraper, Settings


class Scraper(OpenAIBaseScraper[Request, Response]):
    def __init__(
        self,
        openai: AsyncOpenAI | None = None,
        settings: Settings | None = None,
        model: str = "gpt-5-mini",
    ) -> None:
        super().__init__(
            result_type=Response,
            openai=openai,
            settings=settings,
            model=model,
        )

    @override
    async def collect(
        self,
        context: BrowserContext,
        request: Request,
    ) -> str:
        page = await context.new_page()

        await page.goto(request.url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        html = await page.content()
        return html
