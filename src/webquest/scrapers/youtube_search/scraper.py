from typing import override
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from webquest.base_scraper import BaseScraper
from webquest.scrapers.youtube_search.schemas import (
    Channel,
    Post,
    Request,
    Response,
    Short,
    Video,
)


class Scraper(BaseScraper[Request, str, Response]):
    def _parse_videos(self, soup: BeautifulSoup) -> list[Video]:
        videos: list[Video] = []
        video_tags = soup.find_all("ytd-video-renderer")

        for video_tag in video_tags:
            title_tag = video_tag.find(
                "h3",
                class_="title-and-badge style-scope ytd-video-renderer",
            )
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            views_tag, published_at_tag = video_tag.find_all(
                "span",
                class_="inline-metadata-item style-scope ytd-video-meta-block",
            )
            views = views_tag.get_text(strip=True)
            published_at = published_at_tag.get_text(strip=True)

            # length_tag = video_tag.find(
            #     "div",
            #     class_="yt-badge-shape__text",
            # )
            # if not length_tag:
            #     continue
            # length = length_tag.get_text(strip=True)

            description_tag = video_tag.find(
                "yt-formatted-string",
                class_="metadata-snippet-text style-scope ytd-video-renderer",
            )
            if not description_tag:
                continue
            description = description_tag.get_text(strip=True)

            channel_name_tag = video_tag.find(
                "a",
                class_="yt-simple-endpoint style-scope yt-formatted-string",
            )
            if not channel_name_tag:
                continue
            channel_name = channel_name_tag.get_text(strip=True)

            channel_id_tag = video_tag.find(
                "a",
                class_="yt-simple-endpoint style-scope yt-formatted-string",
            )
            if not channel_id_tag:
                continue
            channel_id = channel_id_tag.get("href")
            if not isinstance(channel_id, str):
                continue
            channel_id = channel_id[1:]

            channel_url = f"https://www.youtube.com/{channel_id}"

            video_id_tag = video_tag.find(
                "a",
                class_="yt-simple-endpoint style-scope ytd-video-renderer",
            )
            if not video_id_tag:
                continue
            video_id = video_id_tag.get("href")
            if not isinstance(video_id, str):
                continue
            video_id = video_id.split("v=")[-1].split("&")[0]

            video_url = f"https://www.youtube.com/watch?v={video_id}"

            video = Video(
                id=video_id,
                url=video_url,
                title=title,
                description=description,
                published_at=published_at,
                views=views,
                channel_id=channel_id,
                channel_url=channel_url,
                channel_name=channel_name,
            )
            videos.append(video)
        filtered_videos: list[Video] = []
        for video in videos:
            if len(video.id) != 11:
                continue
            filtered_videos.append(video)
        return filtered_videos

    def _parse_channels(self, soup: BeautifulSoup) -> list[Channel]:
        channels: list[Channel] = []
        # channel_blocks = soup.find_all(
        #     "ytd-channel-renderer",
        #     class_="style-scope ytd-item-section-renderer",
        # )
        # for channel_block in channel_blocks:
        #     channel_name = channel_block.find_all(
        #         "yt-formatted-string",
        #         class_="style-scope ytd-channel-name",
        #     )[0].get_text(strip=True)
        #     description_elem = channel_block.find(
        #         "yt-formatted-string", id="description"
        #     )
        #     description = (
        #         description_elem.get_text(strip=True) if description_elem else None
        #     )
        #     if description == "":
        #         description = None
        #     channel_id = channel_block.find_all(
        #         "yt-formatted-string", id="subscribers"
        #     )[0].get_text(strip=True)
        #     subscribers = channel_block.find_all("span", id="video-count")[0].get_text(
        #         strip=True
        #     )
        #     channel_url = f"https://www.youtube.com/{channel_id}"
        #     channel = Channel(
        #         id=channel_id,
        #         url=channel_url,
        #         name=channel_name,
        #         description=description,
        #         subscribers=subscribers,
        #     )
        #     channels.append(channel)
        return channels

    def _parse_posts(self, soup: BeautifulSoup) -> list[Post]:
        posts: list[Post] = []
        # post_blocks = soup.find_all(
        #     "ytd-post-renderer",
        #     class_="style-scope ytd-item-section-renderer",
        # )
        # for post_block in post_blocks:
        #     post_content = post_block.find_all(
        #         "yt-formatted-string",
        #         id="home-content-text",
        #     )[0].get_text(strip=True)
        #     print(post_content)
        return posts

    def _parse_shorts(self, soup: BeautifulSoup) -> list[Short]:
        shorts: list[Short] = []
        # Implementation for parsing shorts goes here
        return shorts

    def _parse_search_results(self, soup: BeautifulSoup) -> Response:
        videos = self._parse_videos(soup)
        channels = self._parse_channels(soup)
        posts = self._parse_posts(soup)
        shorts = self._parse_shorts(soup)
        return Response(videos=videos, channels=channels, posts=posts, shorts=shorts)

    @override
    async def parse(self, raw: str) -> Response:
        soup = BeautifulSoup(raw, "html.parser")
        result = self._parse_search_results(soup)
        return result

    @override
    async def fetch(self, context: BrowserContext, request: Request) -> str:
        url = (
            f"https://www.youtube.com/results?search_query={quote_plus(request.query)}"
        )
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_selector("ytd-video-renderer", timeout=10000)
        html = await page.content()
        return html
