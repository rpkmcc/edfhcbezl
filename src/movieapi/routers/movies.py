from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from movieapi import schemas, services
from movieapi.constants import BASE_URL
from movieapi.db_core import get_session

router = APIRouter(prefix=BASE_URL)


@router.get(path="/movies/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.MovieOut)
def get_movie(movie_id: int, db_session: Session = Depends(get_session)) -> schemas.MovieOut:
    movie = services.get_movie(movie_id, db_session)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie


@router.get(path="/movies/search", status_code=status.HTTP_200_OK, response_model=schemas.MovieSearchResult)
def get_movies(
    q: str = Query(..., description="Natural language query, e.g. 'recommend action movies from 2020'"),
    db_session: Session = Depends(get_session),
    limit: int = Query(25, ge=1, le=100, description="Max number of results to return"),
):
    movies = services.get_movies(db_session, q, limit)

    return {"query": q, "limit": limit, **movies}
