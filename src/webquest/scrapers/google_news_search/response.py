from pydantic import BaseModel


class Article(BaseModel):
    """
    Represents a news article found in Google News.

    Attributes:
        site: The name of the news site.
        url: The URL of the article.
        title: The title of the article.
        published_at: The publication date of the article.
    """

    site: str
    url: str
    title: str
    published_at: str


class GoogleNewsSearchResponse(BaseModel):
    """
    Represents the response from a Google News search.

    Attributes:
        articles: A list of news articles found.
    """

    articles: list[Article]
