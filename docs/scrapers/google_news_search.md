# Google News Search

Scraper to perform a Google News search and parse the results.

Example usage:

```python
import asyncio
from webquest.browsers import Hyperbrowser
from webquest.scrapers import GoogleNewsSearch

async def main():
    scraper = GoogleNewsSearch(browser=Hyperbrowser())
    response = await scraper.run(
        scraper.request_model(query="Artificial Intelligence"),
    )
    print(response.model_dump_json(indent=4))

if __name__ == "__main__":
    asyncio.run(main())
```

## Settings

**GoogleNewsSearchSettings**

Configuration settings for the Google News search scraper.

| Name | Type | Default | Description |
|---|---|---|---|
| `result_limit` | `int` | `10` |  |
| `character_limit` | `int` | `1000` |  |

## Request

**GoogleNewsSearchRequest**

Represents a request to search Google News.

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | **Required** |  |

## Response

**GoogleNewsSearchResponse**

Represents the response from a Google News search.

| Name | Type | Default | Description |
|---|---|---|---|
| `articles` | `list[Article]` | **Required** |  |

**Article**

Represents a news article found in Google News.

| Name | Type | Default | Description |
|---|---|---|---|
| `site` | `str` | **Required** |  |
| `url` | `str` | **Required** |  |
| `title` | `str` | **Required** |  |
| `published_at` | `str` | **Required** |  |
