# YouTube Transcript

Scraper to extract the transcript of a YouTube video.

## Settings

**YouTubeTranscriptSettings**



| Name | Type | Default | Description |
|---|---|---|---|
| `character_limit` | `int` | `5000` |  |

## Request

**YouTubeTranscriptRequest**



| Name | Type | Default | Description |
|---|---|---|---|
| `video_id` | `str` | **Required** |  |

## Response

**YouTubeTranscriptResponse**



| Name | Type | Default | Description |
|---|---|---|---|
| `transcript` | `str` | **Required** |  |