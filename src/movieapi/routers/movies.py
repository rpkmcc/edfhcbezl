from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from movieapi import schemas, services
from movieapi.constants import BASE_URL
from movieapi.db_core import get_session

router = APIRouter(prefix=BASE_URL)


@router.get(path="/movies/search", status_code=status.HTTP_200_OK, response_model=schemas.MovieSearchResponse)
def get_movies(
    q: str = Query(
        ..., description="Natural language query, e.g. 'recommend action movies from 2018 | recommend movies above 4.8'"
    ),
    db_session: Session = Depends(get_session),
    limit: int = Query(25, ge=1, le=100, description="Max number of results to return"),
):
    movies = services.get_movies(db_session, q, limit)

    if len(movies.get("results", [])) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No matching movies found")
    return {"query": q, "limit": limit, **movies}


@router.get(path="/movies/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.MovieOut)
def get_movie(
    movie_id: int = Path(..., ge=1, description="The movie ID (must be a positive integer)"),
    db_session: Session = Depends(get_session),
) -> schemas.MovieOut:
    movie = services.get_movie(movie_id, db_session)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie
