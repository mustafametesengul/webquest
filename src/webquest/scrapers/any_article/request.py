from pydantic import BaseModel


class AnyArticleRequest(BaseModel):
    """
    Represents a request to extract an article from a web page.
    """

    url: str
