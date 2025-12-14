from pydantic import BaseModel


class YouTubeSearchRequest(BaseModel):
    """
    Represents a request to search YouTube.
    """

    query: str
