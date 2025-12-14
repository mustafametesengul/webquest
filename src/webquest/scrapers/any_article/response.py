from pydantic import BaseModel


class AnyArticleResponse(BaseModel):
    """
    Represents the extracted article content.
    """

    publisher: str
    title: str
    published_at: str
    authors: list[str]
    content: str
