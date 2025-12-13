from pydantic import BaseModel


class YouTubeSearchRequest(BaseModel):
    """
    Represents a request to search YouTube.

    Attributes:
        query: The search query string.
    """

    query: str
