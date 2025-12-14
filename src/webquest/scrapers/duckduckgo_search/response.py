from pydantic import BaseModel


class Page(BaseModel):
    """
    Represents a web page found in DuckDuckGo search results.
    """

    site: str
    url: str
    title: str
    description: str


class DuckDuckGoSearchResponse(BaseModel):
    """
    Represents the response from a DuckDuckGo search.
    """

    pages: list[Page]
