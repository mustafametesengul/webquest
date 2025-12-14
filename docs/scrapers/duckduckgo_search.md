# DuckDuckGo Search

Scraper to perform a DuckDuckGo web search and parse the results.

## Settings

### DuckDuckGoSearchSettings



| Name | Type | Default | Description |
|---|---|---|---|
| `result_limit` | `int` | `10` |  |
| `character_limit` | `int` | `1000` |  |

## Request

### DuckDuckGoSearchRequest



| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | **Required** |  |

## Response

### DuckDuckGoSearchResponse



| Name | Type | Default | Description |
|---|---|---|---|
| `pages` | `list[Page]` | **Required** |  |

### Page



| Name | Type | Default | Description |
|---|---|---|---|
| `site` | `str` | **Required** |  |
| `url` | `str` | **Required** |  |
| `title` | `str` | **Required** |  |
| `description` | `str` | **Required** |  |
