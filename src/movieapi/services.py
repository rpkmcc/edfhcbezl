from sqlalchemy.orm import Session

from movieapi.models import Movie


def get_movie(movie_id: int, session: Session) -> Movie | None:
    movie = session.get(Movie, movie_id)
    return movie
