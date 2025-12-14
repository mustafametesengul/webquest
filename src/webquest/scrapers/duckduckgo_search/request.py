from pydantic import BaseModel


class DuckDuckGoSearchRequest(BaseModel):
    """
    Represents a request to search DuckDuckGo.
    """

    query: str
