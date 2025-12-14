# Any Article

Scraper to extract the main article from any web page using OpenAI.

## Settings

### AnyArticleSettings



| Name | Type | Default | Description |
|---|---|---|---|
| `character_limit` | `int` | `5000` |  |
| `parser_model` | `str` | `gpt-5-mini` |  |
| `openai_api_key` | `SecretStr | None` | `None` |  |

## Request

### AnyArticleRequest



| Name | Type | Default | Description |
|---|---|---|---|
| `url` | `str` | **Required** |  |

## Response

### AnyArticleResponse



| Name | Type | Default | Description |
|---|---|---|---|
| `publisher` | `str` | **Required** |  |
| `title` | `str` | **Required** |  |
| `published_at` | `str` | **Required** |  |
| `authors` | `list[str]` | **Required** |  |
| `content` | `str` | **Required** |  |