# YouTube Search

Scraper to perform a YouTube search and parse the results.

Examples:
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
| `query` | `str` | **Required** |  |

## Response

**YouTubeSearchResponse**

Represents the response from a YouTube search.

| Name | Type | Default | Description |
|---|---|---|---|
| `videos` | `list[Video]` | **Required** |  |
| `channels` | `list[Channel]` | **Required** |  |
| `posts` | `list[Post]` | **Required** |  |
| `shorts` | `list[Short]` | **Required** |  |

**Channel**

Represents a YouTube channel.

| Name | Type | Default | Description |
|---|---|---|---|
| `id` | `str` | **Required** |  |
| `url` | `str` | **Required** |  |
| `name` | `str` | **Required** |  |
| `description` | `str | None` | **Required** |  |
| `subscribers` | `str` | **Required** |  |

**Post**

Represents a YouTube community post.

| Name | Type | Default | Description |
|---|---|---|---|
| `id` | `str` | **Required** |  |
| `url` | `str` | **Required** |  |
| `content` | `str` | **Required** |  |
| `published_at` | `str` | **Required** |  |
| `channel_id` | `str` | **Required** |  |
| `channel_url` | `str` | **Required** |  |
| `channel_name` | `str` | **Required** |  |
| `comments` | `str` | **Required** |  |
| `likes` | `str` | **Required** |  |

**Short**

Represents a YouTube Short.

| Name | Type | Default | Description |
|---|---|---|---|
| `id` | `str` | **Required** |  |
| `url` | `str` | **Required** |  |
| `title` | `str` | **Required** |  |
| `views` | `str` | **Required** |  |

**Video**

Represents a YouTube video.

| Name | Type | Default | Description |
|---|---|---|---|
| `id` | `str` | **Required** |  |
| `url` | `str` | **Required** |  |
| `title` | `str` | **Required** |  |
| `description` | `str` | **Required** |  |
| `published_at` | `str` | **Required** |  |
| `views` | `str` | **Required** |  |
| `channel_id` | `str` | **Required** |  |
| `channel_url` | `str` | **Required** |  |
| `channel_name` | `str` | **Required** |  |
