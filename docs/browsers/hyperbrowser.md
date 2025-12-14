# Hyperbrowser

A Browser implementation that uses Hyperbrowser for remote browser sessions.

This class manages the creation and cleanup of Hyperbrowser sessions and provides
a Playwright BrowserContext connected to the remote session.

Example usage:

```python
import asyncio
from webquest.browsers import Hyperbrowser

async def main():
    browser = Hyperbrowser()
    async with browser.get_context() as context:
        page = await context.new_page()
        await page.goto("https://example.com")
        print(await page.title())

if __name__ == "__main__":
    asyncio.run(main())
```

## Settings

**HyperbrowserSettings**

Configuration settings for the Hyperbrowser.

| Name | Type | Default | Description |
|---|---|---|---|
| `hyperbrowser_api_key` | `SecretStr | None` | `None` | The API key for Hyperbrowser. |
| `max_concurrent_sessions` | `int` | `5` | The maximum number of concurrent sessions. |