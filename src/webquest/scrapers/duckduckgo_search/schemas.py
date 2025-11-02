from pydantic import BaseModel


class Request(BaseModel):
    query: str


class Page(BaseModel):
    site: str
    url: str
    title: str
    description: str


class Result(BaseModel):
    pages: list[Page]
