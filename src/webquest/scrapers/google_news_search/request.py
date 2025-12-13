from pydantic import BaseModel


class GoogleNewsSearchRequest(BaseModel):
    """
    Represents a request to search Google News.

    Attributes:
        query: The search query string.
    """

    query: str
