from sqlalchemy import select
from sqlalchemy.orm import Session

from movieapi.models import Movie


def get_movie(movie_id: int, session: Session) -> Movie | None:
    try:
        movie = session.scalars(select(Movie).where(Movie.movie_id == movie_id)).first()
        return movie
    except Exception as er:
        print(f"{er}")
