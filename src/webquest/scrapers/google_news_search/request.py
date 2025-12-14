from pydantic import BaseModel


class GoogleNewsSearchRequest(BaseModel):
    """
    Represents a request to search Google News.
    """

    query: str
