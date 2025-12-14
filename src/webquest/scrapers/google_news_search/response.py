from pydantic import BaseModel


class Article(BaseModel):
    """
    Represents a news article found in Google News.
    """

    site: str
    url: str
    title: str
    published_at: str


class GoogleNewsSearchResponse(BaseModel):
    """
    Represents the response from a Google News search.
    """

    articles: list[Article]
