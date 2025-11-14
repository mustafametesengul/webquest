from typing import override

from openai import AsyncOpenAI
from playwright.async_api import BrowserContext

from webquest.scrapers.any_article.schemas import AnyArticleRequest, AnyArticleResponse
from webquest.scrapers.openai_parser import OpenAIParser, OpenAIParserSettings


class AnyArticle(OpenAIParser[AnyArticleRequest, AnyArticleResponse]):
    def __init__(
        self,
        openai: AsyncOpenAI | None = None,
        settings: OpenAIParserSettings | None = None,
        model: str = "gpt-5-mini",
    ) -> None:
        super().__init__(
            response_type=AnyArticleResponse,
            openai=openai,
            settings=settings,
            model=model,
            input="Parse the following web page and extract the main article:\n\n",
        )

    @override
    async def fetch(
        self,
        context: BrowserContext,
        request: AnyArticleRequest,
    ) -> str:
        page = await context.new_page()
        await page.goto(request.url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        html = await page.content()
        return html
