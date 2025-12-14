# Google News Search

Scraper to perform a Google News search and parse the results.

Examples:
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

### GoogleNewsSearchSettings

Configuration settings for the Google News search scraper.

Attributes:
    result_limit: The maximum number of results to return. Defaults to 10.
    character_limit: The maximum number of characters to parse. Defaults to 1000.

| Name | Type | Default | Description |
|---|---|---|---|
| `result_limit` | `int` | `10` |  |
| `character_limit` | `int` | `1000` |  |

## Request

### GoogleNewsSearchRequest

Represents a request to search Google News.

Attributes:
    query: The search query string.

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | **Required** |  |

## Response

### GoogleNewsSearchResponse

Represents the response from a Google News search.

Attributes:
    articles: A list of news articles found.

| Name | Type | Default | Description |
|---|---|---|---|
| `articles` | `list[Article]` | **Required** |  |

### Article

Represents a news article found in Google News.

Attributes:
    site: The name of the news site.
    url: The URL of the article.
    title: The title of the article.
    published_at: The publication date of the article.

| Name | Type | Default | Description |
|---|---|---|---|
| `site` | `str` | **Required** |  |
| `url` | `str` | **Required** |  |
| `title` | `str` | **Required** |  |
| `published_at` | `str` | **Required** |  |
