from pydantic import BaseModel


class Request(BaseModel):
    url: str


class Response(BaseModel):
    publisher: str
    title: str
    published_at: str
    authors: list[str]
    content: str
