from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from movieapi import schemas, services
from movieapi.constants import BASE_URL
from movieapi.db_tables import create_sql_engine

router = APIRouter(prefix=BASE_URL)


def get_session() -> Session:
    create_sql_engine()


@router.get(path="/movies/{movie_id}", status_code=status.HTTP_200_OK, response_model=schemas.MovieOut)
def get_movie(movie_id: int, db_session: Session):
    movie = services.get_movie(movie_id, db_session)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie
