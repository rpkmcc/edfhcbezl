from typing import Optional

from pydantic import BaseModel


class GenreOut(BaseModel):
    name: str


class MovieOut(BaseModel):
    movie_id: int
    title: str
    year: int
    genres: Optional[list[GenreOut] | list[str]] = None
    rating: Optional[float] = None


# --- shows how the text query was parsed ---
class ParsedQuery(BaseModel):
    intent: str
    genre: Optional[str] = None
    year: Optional[int] = None
    title: Optional[str] = None
    rating: Optional[float] = None


# --- full response model for /movies/search ---
class MovieSearchResponse(BaseModel):
    query: str
    limit: int
    parsed: ParsedQuery
    results: list[MovieOut]
