import asyncio
from typing import override

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from webquest.base import BaseScraper
from webquest.scrapers.youtube_transcript.schemas import Request, Response


class Scraper(BaseScraper[Request, str, Response]):
    @override
    async def collect(
        self,
        context: BrowserContext,
        request: Request,
    ) -> str:
        video_url = f"https://www.youtube.com/watch?v={request.video_id}"

        page = await context.new_page()

        await page.goto(video_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)

        # Try to expand description
        try:
            await page.wait_for_selector("div#description", timeout=10000)
            await page.click("div#description")
        except Exception:
            pass

        await asyncio.sleep(0.5)

        # Click "Show transcript"
        try:
            transcript_button = await page.wait_for_selector(
                'button[aria-label="Show transcript"]', timeout=10000
            )
            if not transcript_button:
                raise Exception()
        except Exception:
            raise Exception(
                "Transcript button not found — transcript may not be available"
            )

        await transcript_button.click()

        # Wait for transcript
        await page.wait_for_selector(
            "ytd-transcript-segment-list-renderer", timeout=10000
        )

        html = await page.content()
        return html

    @override
    async def parse(self, collection: str) -> Response:
        soup = BeautifulSoup(collection, "html.parser")

        # Find the transcript segment list renderer
        segment_renderer = soup.select_one("ytd-transcript-segment-list-renderer")
        if not segment_renderer:
            raise Exception("No transcript segments found")

        # Find the segments container
        segments_container = segment_renderer.select_one("div#segments-container")
        if not segments_container:
            raise Exception("No transcript segments found")

        # Find all transcript segment renderers
        segments = segments_container.select("ytd-transcript-segment-renderer")
        if not segments:
            raise Exception("No transcript segments found")

        # Extract text from each segment
        transcript_segments = []
        for segment in segments:
            text_element = segment.select_one("yt-formatted-string")
            if text_element:
                transcript_segments.append(text_element.get_text())

        formatted_transcript = " ".join(transcript_segments).strip()
        result = Response(transcript=formatted_transcript)

        return result
