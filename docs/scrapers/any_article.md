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
| `character_limit` | `int` | `5000` | The maximum number of characters to parse. |
| `parser_model` | `str` | `gpt-5-mini` | The OpenAI model to use for parsing. |
| `openai_api_key` | `SecretStr | None` | `None` | The API key for OpenAI. |

## Request

**AnyArticleRequest**

Represents a request to extract an article from a web page.

| Name | Type | Default | Description |
|---|---|---|---|
| `url` | `str` | **Required** | The URL of the web page to extract the article from. |

## Response

**AnyArticleResponse**

Represents the extracted article content.

| Name | Type | Default | Description |
|---|---|---|---|
| `publisher` | `str` | **Required** | The name of the publisher. |
| `title` | `str` | **Required** | The title of the article. |
| `published_at` | `str` | **Required** | The publication date of the article. |
| `authors` | `list[str]` | **Required** | The list of authors of the article. |
| `content` | `str` | **Required** | The main content of the article. |