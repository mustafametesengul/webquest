# WebQuest

WebQuest is an extensible Python toolkit for high-level web scraping, built around a generic Playwright-based scraper interface for quickly building, running, and reusing custom scrapers.

Scrapers:

- Any Article
- DuckDuckGo Search
- Google News Search
- YouTube Search
- YouTube Transcript

Runners:

- Hyperbrowser

## Installation

Installing using pip:

```bash
pip install webquest
```

Installing using uv:

```bash
uv add webquest
```

## Usage

Example usage of the DuckDuckGo Search scraper:

```python
import asyncio

from webquest.runners import Hyperbrowser
from webquest.scrapers import DuckDuckGoSearch, DuckDuckGoSearchRequest


async def main() -> None:
    runner = Hyperbrowser()
    scraper = DuckDuckGoSearch()
    response = await runner.run(
        scraper,
        DuckDuckGoSearchRequest(query="Pizza Toppings"),
    )
    print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
```

> To use the Hyperbrowser runner, you need to set the `HYPERBROWSER_API_KEY` environment variable.

You can also run multiple requests at the same time:

```python
import asyncio

from webquest.runners import Hyperbrowser
from webquest.scrapers import DuckDuckGoSearch, DuckDuckGoSearchRequest


async def main() -> None:
    runner = Hyperbrowser()
    scraper = DuckDuckGoSearch()
    responses = await runner.run_multiple(
        scraper,
        [
            DuckDuckGoSearchRequest(query="Pizza Toppings"),
            DuckDuckGoSearchRequest(query="AI News"),
        ],
    )
    for response in responses:
        print(response.model_dump_json(indent=4))


if __name__ == "__main__":
    asyncio.run(main())
```
