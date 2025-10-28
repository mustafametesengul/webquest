import asyncio

import webquest.scrapers.duckduckgo as duckduckgo
import webquest.scrapers.youtube as youtube
from webquest.browser_managers.hyperbrowser_manager import HyperbrowserManager


async def main() -> None:
    async with HyperbrowserManager() as browser_manager:
        ddg = duckduckgo.SearchScraper(browser_manager)
        yt = youtube.TranscriptScraper(browser_manager)

        r1, r2 = await asyncio.gather(
            ddg.run(duckduckgo.SearchRequest(query="Moist Critical")),
            yt.run(youtube.TranscriptRequest(video_id="Vg65n2wqikI")),
        )

        print(r1.model_dump_json(indent=4))
        print(r2.transcript[:100])


if __name__ == "__main__":
    asyncio.run(main())
