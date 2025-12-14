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

### YouTubeSearchSettings

Configuration settings for the YouTube search scraper.

| Name | Type | Default | Description |
|---|---|---|---|
| `result_limit` | `int` | `10` | The maximum number of results to return. |
| `character_limit` | `int` | `1000` | The maximum number of characters to parse. |

## Request

### YouTubeSearchRequest

Represents a request to search YouTube.

Attributes:
    query: The search query string.

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | **Required** |  |

## Response

### YouTubeSearchResponse

Represents the response from a YouTube search.

Attributes:
    videos: A list of videos found.
    channels: A list of channels found.
    posts: A list of community posts found.
    shorts: A list of shorts found.

| Name | Type | Default | Description |
|---|---|---|---|
| `videos` | `list[Video]` | **Required** |  |
| `channels` | `list[Channel]` | **Required** |  |
| `posts` | `list[Post]` | **Required** |  |
| `shorts` | `list[Short]` | **Required** |  |

### Channel

Represents a YouTube channel.

Attributes:
    id: The unique identifier of the channel.
    url: The URL of the channel.
    name: The name of the channel.
    description: The description of the channel.
    subscribers: The subscriber count of the channel.

| Name | Type | Default | Description |
|---|---|---|---|
| `id` | `str` | **Required** |  |
| `url` | `str` | **Required** |  |
| `name` | `str` | **Required** |  |
| `description` | `str | None` | **Required** |  |
| `subscribers` | `str` | **Required** |  |

### Post

Represents a YouTube community post.

Attributes:
    id: The unique identifier of the post.
    url: The URL of the post.
    content: The content of the post.
    published_at: The publication date of the post.
    channel_id: The ID of the channel that created the post.
    channel_url: The URL of the channel.
    channel_name: The name of the channel.
    comments: The comment count of the post.
    likes: The like count of the post.

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

### Short

Represents a YouTube Short.

Attributes:
    id: The unique identifier of the short.
    url: The URL of the short.
    title: The title of the short.
    views: The view count of the short.

| Name | Type | Default | Description |
|---|---|---|---|
| `id` | `str` | **Required** |  |
| `url` | `str` | **Required** |  |
| `title` | `str` | **Required** |  |
| `views` | `str` | **Required** |  |

### Video

Represents a YouTube video.

Attributes:
    id: The unique identifier of the video.
    url: The URL of the video.
    title: The title of the video.
    description: The description of the video.
    published_at: The publication date of the video.
    views: The view count of the video.
    channel_id: The ID of the channel that uploaded the video.
    channel_url: The URL of the channel.
    channel_name: The name of the channel.

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
