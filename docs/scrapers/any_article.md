# Any Article

Scraper to extract the main article from any web page using OpenAI.

Example usage:

```python
import asyncio
from webquest.browsers import Hyperbrowser
from webquest.scrapers import AnyArticle

async def main():
    scraper = AnyArticle(browser=Hyperbrowser())
    response = await scraper.run(
        scraper.request_model(url="https://example.com/article"),
    )
    print(response.model_dump_json(indent=4))

if __name__ == "__main__":
    asyncio.run(main())
```

## Settings

**AnyArticleSettings**

Configuration settings for the Any Article scraper.

| Name | Type | Default | Description |
|---|---|---|---|
| `character_limit` | `int` | `5000` |  |
| `parser_model` | `str` | `gpt-5-mini` |  |
| `openai_api_key` | `SecretStr | None` | `None` |  |

## Request

**AnyArticleRequest**

Represents a request to extract an article from a web page.

| Name | Type | Default | Description |
|---|---|---|---|
| `url` | `str` | **Required** |  |

## Response

**AnyArticleResponse**

Represents the extracted article content.

| Name | Type | Default | Description |
|---|---|---|---|
| `publisher` | `str` | **Required** |  |
| `title` | `str` | **Required** |  |
| `published_at` | `str` | **Required** |  |
| `authors` | `list[str]` | **Required** |  |
| `content` | `str` | **Required** |  |