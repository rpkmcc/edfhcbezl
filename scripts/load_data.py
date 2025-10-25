import csv
import re
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from movieapi.constants import MOVIES_CSV_PATH, RATINGS_CSV_PATH, SQLITE_DB_FILE
from movieapi.db_tables import create_sql_engine, init_db, start_mappers
from movieapi.models import Genre, Movie, Rating

YEAR_RE: re.Pattern = re.compile(r"\((\d{4})\)\s*$")


def get_session_factory(db_url=SQLITE_DB_FILE) -> sessionmaker[Session]:
    start_mappers()
    engine = create_sql_engine(url=db_url)
    init_db(engine)
    return sessionmaker(bind=engine)


@contextmanager
def session_scope(SessionFactory: sessionmaker[Session]):
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


def extract_title_and_year(raw_title: str) -> tuple[str, int | None]:
    """MovieLens titles end with ' (YYYY)' –  pull out the year."""
    if len(raw_title) == 0 and not isinstance(raw_title, str):
        return ("", None)
    match = YEAR_RE.search(raw_title)
    if match is not None:
        year = int(match.group(1))
        title = YEAR_RE.sub("", raw_title).strip()
        return (title, year)
    return (raw_title, None)


def parse_genres(genres: str) -> list[str]:
    if not isinstance(genres, str):
        return []

    genres_filtered = [g.lower() for g in genres.split("|") if len(g) != 0 and g.lower() != "no genres listed"]
    return genres_filtered


def load_movies_data(session: Session, csv_path: Path):
    try:
        genre_cache: dict[str, Genre] = {}
        with open(csv_path, newline="", encoding="utf-8") as fd:
            csv_data = csv.DictReader(fd)

            for i, row in enumerate(csv_data):
                movie_id = int(row.get("movieId"))
                title, year = extract_title_and_year(row.get("title"))

                if movie_id is None:
                    continue
                movie = Movie(movie_id, title, year)
                session.add(movie)
                session.flush()

                genres = row.get("genres")
                for name in parse_genres(genres):
                    genre = genre_cache.get(name)
                    if genre is None:
                        genre = Genre(name)
                        genre_cache[name] = genre
                        session.add(genre)
                        session.flush()

                    movie.genres.append(genre)

                if i % 2000 == 0:
                    session.commit()
        session.commit()

    except OSError:
        pass


def get_movie_id_to_pk(session: Session) -> dict[int, int]:
    stmt = select(Movie.movie_id, Movie.id)
    rows = session.execute(stmt)
    return {movie_id: pk for (movie_id, pk) in rows}


def load_ratings_data(session: Session, csv_path: Path):
    movie_id_to_pk = get_movie_id_to_pk(session)

    with csv_path.open(newline="", encoding="utf-8") as fd:
        csv_data = csv.DictReader(fd)
        for i, row in enumerate(csv_data):
            pk = movie_id_to_pk.get(int(row.get("movieId")))
            if pk is None:
                continue
            rating = Rating(int(row.get("userId")), float(row.get("rating")), int(row.get("timestamp")))
            rating.movie_id = pk
            session.add(rating)

            if i % 2000 == 0:
                session.commit()
    session.commit()


if __name__ == "__main__":
    Sess: sessionmaker[Session] = get_session_factory()

    with session_scope(Sess) as db:
        load_movies_data(db, MOVIES_CSV_PATH)
        load_ratings_data(db, RATINGS_CSV_PATH)
