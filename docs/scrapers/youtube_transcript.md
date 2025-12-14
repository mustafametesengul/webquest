# YouTube Transcript

Scraper to extract the transcript of a YouTube video.

Example usage:

```python
import asyncio
from webquest.browsers import Hyperbrowser
from webquest.scrapers import YouTubeTranscript

async def main():
    scraper = YouTubeTranscript(browser=Hyperbrowser())
    response = await scraper.run(
        scraper.request_model(video_id="dQw4w9WgXcQ"),
    )
    print(response.model_dump_json(indent=4))

if __name__ == "__main__":
    asyncio.run(main())
```

## Settings

**YouTubeTranscriptSettings**

Configuration settings for the YouTube transcript scraper.

| Name | Type | Default | Description |
|---|---|---|---|
| `character_limit` | `int` | `5000` |  |

## Request

**YouTubeTranscriptRequest**

Represents a request to extract the transcript of a YouTube video.

| Name | Type | Default | Description |
|---|---|---|---|
| `video_id` | `str` | **Required** |  |

## Response

**YouTubeTranscriptResponse**

Represents the extracted transcript of a YouTube video.

| Name | Type | Default | Description |
|---|---|---|---|
| `transcript` | `str` | **Required** |  |