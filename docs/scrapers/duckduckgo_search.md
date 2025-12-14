# DuckDuckGo Search

Scraper to perform a DuckDuckGo web search and parse the results.

Example usage:

```python
import asyncio
from webquest.browsers import Hyperbrowser
from webquest.scrapers import DuckDuckGoSearch

async def main():
    scraper = DuckDuckGoSearch(browser=Hyperbrowser())
    response = await scraper.run(
        scraper.request_model(query="Python programming"),
    )
    print(response.model_dump_json(indent=4))

if __name__ == "__main__":
    asyncio.run(main())
```

## Settings

**DuckDuckGoSearchSettings**

Configuration settings for the DuckDuckGo search scraper.

| Name | Type | Default | Description |
|---|---|---|---|
| `result_limit` | `int` | `10` |  |
| `character_limit` | `int` | `1000` |  |

## Request

**DuckDuckGoSearchRequest**

Represents a request to search DuckDuckGo.

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | **Required** |  |

## Response

**DuckDuckGoSearchResponse**

Represents the response from a DuckDuckGo search.

| Name | Type | Default | Description |
|---|---|---|---|
| `pages` | `list[Page]` | **Required** |  |

**Page**

Represents a web page found in DuckDuckGo search results.

| Name | Type | Default | Description |
|---|---|---|---|
| `site` | `str` | **Required** |  |
| `url` | `str` | **Required** |  |
| `title` | `str` | **Required** |  |
| `description` | `str` | **Required** |  |
