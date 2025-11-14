from pydantic import BaseModel


class Request(BaseModel):
    query: str


class Page(BaseModel):
    site: str
    url: str
    title: str
    description: str


class Response(BaseModel):
    pages: list[Page]
