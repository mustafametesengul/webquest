# Hyperbrowser

A Browser implementation that uses Hyperbrowser for remote browser sessions.

This class manages the creation and cleanup of Hyperbrowser sessions and provides
a Playwright BrowserContext connected to the remote session.

## Settings

### HyperbrowserSettings



| Name | Type | Default | Description |
|---|---|---|---|
| `hyperbrowser_api_key` | `SecretStr | None` | `None` |  |
| `max_concurrent_sessions` | `int` | `5` |  |