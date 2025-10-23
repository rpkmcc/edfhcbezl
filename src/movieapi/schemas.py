from typing import Optional

from pydantic import BaseModel


class PageMeta(BaseModel):
    page: int
    page_size: int
    total: int


class MovieOut(BaseModel):
    id: int
    title: str
    year: Optional[int] = None
    genres: Optional[list[str]] = None
    rating: Optional[float] = None


class MovieListOut(BaseModel):
    meta: PageMeta
    items: list[MovieOut]
