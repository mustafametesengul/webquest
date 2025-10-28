import asyncio
import logging
from typing import override

from playwright.async_api import BrowserContext

from webquest.base import Scraper
from webquest.scrapers.youtube.schemas import (
    TranscriptRequest,
    TranscriptResult,
)

logger = logging.getLogger(__name__)


class TranscriptScraper(Scraper[TranscriptRequest, TranscriptResult]):
    @override
    async def scrape(
        self,
        context: BrowserContext,
        request: TranscriptRequest,
    ) -> TranscriptResult:
        video_url = f"https://www.youtube.com/watch?v={request.video_id}"

        page = await context.new_page()

        logger.debug(f"Loading video page: {video_url}")
        await page.goto(video_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)

        # Try to expand description
        try:
            await page.wait_for_selector("div#description", timeout=10000)
            await page.click("div#description")
            logger.debug("Description expanded")
        except Exception:
            logger.debug("Description not found — skipping expansion")

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
        logger.debug("Transcript panel opened")

        # Wait for transcript
        await page.wait_for_selector(
            "ytd-transcript-segment-list-renderer", timeout=10000
        )
        logger.debug("Extracting transcript segments...")

        transcript_segments = await page.evaluate("""() => {
            const segmentRenderer = document.querySelector("ytd-transcript-segment-list-renderer");
            if (!segmentRenderer) return [];
            const segmentsContainer = segmentRenderer.querySelector("div#segments-container");
            if (!segmentsContainer) return [];
            const segments = segmentsContainer.querySelectorAll("ytd-transcript-segment-renderer");
            return Array.from(segments).map(segment => {
                const textElement = segment.querySelector("yt-formatted-string");
                return textElement ? textElement.innerText : "";
            });
        }""")

        if not transcript_segments:
            raise Exception("No transcript segments found")

        logger.debug(f"Found {len(transcript_segments)} transcript segments")

        formatted_transcript = " ".join(transcript_segments).strip()
        result = TranscriptResult(transcript=formatted_transcript)

        return result
