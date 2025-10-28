import asyncio
from typing import override
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from webquest.base import Scraper
from webquest.scrapers.duckduckgo.schemas import (
    Page,
    SearchRequest,
    SearchResult,
)


class SearchScraper(Scraper[SearchRequest, SearchResult]):
    def _parse_search_results(self, html: str) -> SearchResult:
        """Parse search results HTML and extract structured data."""
        soup = BeautifulSoup(html, "html.parser")
        pages = []

        # Find all article elements with the result testid
        articles = soup.find_all("article", {"data-testid": "result"})

        for article in articles:
            # Extract site title
            site_title_elem = article.find("p", class_="fOCEb2mA3YZTJXXjpgdS")
            site_title = site_title_elem.get_text(strip=True) if site_title_elem else ""

            # Extract URL
            url_link = article.find("a", {"data-testid": "result-title-a"})
            url = str(url_link.get("href", "") if url_link else "")

            # Extract title
            title_elem = article.find("span", class_="EKtkFWMYpwzMKOYr0GYm")
            title = title_elem.get_text(strip=True) if title_elem else ""

            # Extract description
            desc_elem = article.find("span", class_="kY2IgmnCmOGjharHErah")
            if desc_elem:
                # Remove bold tags and get clean text
                description = desc_elem.get_text(strip=True)
            else:
                description = ""

            # Create Page object
            page = Page(
                site_title=site_title,
                url=url,
                title=title,
                description=description,
            )
            pages.append(page)

        return SearchResult(pages=pages)

    @override
    async def scrape(
        self,
        context: BrowserContext,
        request: SearchRequest,
    ) -> SearchResult:
        url = f"https://duckduckgo.com/?origin=funnel_home_website&t=h_&q={quote_plus(request.query)}&ia=web"
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)

        await page.wait_for_selector("button#more-results", timeout=15000)
        await page.click("button#more-results")

        await page.wait_for_selector("li[data-layout='organic']", timeout=15000)

        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(4)

        html = await page.content()

        result = self._parse_search_results(html)
        return result
