from typing import Optional

from pydantic import BaseModel


class PageMeta(BaseModel):
    page: int
    page_size: int
    total: int


class GenreOut(BaseModel):
    name: str


class MovieOut(BaseModel):
    movie_id: int
    title: str
    year: int
    genres: Optional[list[GenreOut]] = None
    rating: Optional[float] = None


class MovieListOut(BaseModel):
    meta: PageMeta
    items: list[MovieOut]
