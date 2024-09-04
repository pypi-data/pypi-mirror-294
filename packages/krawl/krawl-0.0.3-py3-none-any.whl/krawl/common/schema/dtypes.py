from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class TagEnum(str, Enum):
    class_ = "class"
    href = "href"
    url = "a"
    id_ = "id"


class HTMLNodeContext(BaseModel):
    tag: str
    classname: str
    idname: str
    wordcount: int
    href: str = ""


class CrawlResponse(BaseModel):
    first: str
    items: List[str]


class Href(BaseModel):
    text: str
    url: str


class StructuredResponse(BaseModel):
    title: str
    h1: List[str]
    h2: List[str]
    text: str
    links: List[Href]
    coretext: str
    image_url_primary: str = Field("")
    """URL of the primary image"""


class StructuredResponseGroup(BaseModel):
    first: StructuredResponse
    items: List[StructuredResponse]
