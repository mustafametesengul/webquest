from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str


class Page(BaseModel):
    site_title: str
    url: str
    title: str
    description: str


class SearchResult(BaseModel):
    pages: list[Page]
