# YouTube Search

Scraper to perform a YouTube search and parse the results.

Example usage:

```python
import asyncio
from webquest.browsers import Hyperbrowser
from webquest.scrapers import YouTubeSearch

async def main():
    scraper = YouTubeSearch(browser=Hyperbrowser())
    response = await scraper.run(
        scraper.request_model(query="Artificial Intelligence"),
    )
    print(response.model_dump_json(indent=4))

if __name__ == "__main__":
    asyncio.run(main())
```

## Settings

**YouTubeSearchSettings**

Configuration settings for the YouTube search scraper.

| Name | Type | Default | Description |
|---|---|---|---|
| `result_limit` | `int` | `10` | The maximum number of results to return. |
| `character_limit` | `int` | `1000` | The maximum number of characters to parse. |

## Request

**YouTubeSearchRequest**

Represents a request to search YouTube.

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | **Required** | The search query. |

## Response

**YouTubeSearchResponse**

Represents the response from a YouTube search.

| Name | Type | Default | Description |
|---|---|---|---|
| `videos` | `list[Video]` | **Required** | The list of videos found. |
| `channels` | `list[Channel]` | **Required** | The list of channels found. |
| `posts` | `list[Post]` | **Required** | The list of posts found. |
| `shorts` | `list[Short]` | **Required** | The list of shorts found. |

**Channel**

Represents a YouTube channel.

| Name | Type | Default | Description |
|---|---|---|---|
| `id` | `str` | **Required** | The channel ID. |
| `url` | `str` | **Required** | The URL of the channel. |
| `name` | `str` | **Required** | The name of the channel. |
| `description` | `str | None` | `None` | The description of the channel. |
| `subscribers` | `str` | **Required** | The number of subscribers. |

**Post**

Represents a YouTube community post.

| Name | Type | Default | Description |
|---|---|---|---|
| `id` | `str` | **Required** | The post ID. |
| `url` | `str` | **Required** | The URL of the post. |
| `content` | `str` | **Required** | The content of the post. |
| `published_at` | `str` | **Required** | The publication date of the post. |
| `channel_id` | `str` | **Required** | The channel ID. |
| `channel_url` | `str` | **Required** | The URL of the channel. |
| `channel_name` | `str` | **Required** | The name of the channel. |
| `comments` | `str` | **Required** | The number of comments. |
| `likes` | `str` | **Required** | The number of likes. |

**Short**

Represents a YouTube Short.

| Name | Type | Default | Description |
|---|---|---|---|
| `id` | `str` | **Required** | The short ID. |
| `url` | `str` | **Required** | The URL of the short. |
| `title` | `str` | **Required** | The title of the short. |
| `views` | `str` | **Required** | The number of views. |

**Video**

Represents a YouTube video.

| Name | Type | Default | Description |
|---|---|---|---|
| `id` | `str` | **Required** | The video ID. |
| `url` | `str` | **Required** | The URL of the video. |
| `title` | `str` | **Required** | The title of the video. |
| `description` | `str` | **Required** | The description of the video. |
| `published_at` | `str` | **Required** | The publication date of the video. |
| `views` | `str` | **Required** | The number of views. |
| `channel_id` | `str` | **Required** | The channel ID. |
| `channel_url` | `str` | **Required** | The URL of the channel. |
| `channel_name` | `str` | **Required** | The name of the channel. |
