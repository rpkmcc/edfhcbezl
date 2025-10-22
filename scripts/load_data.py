import csv
import re

from sqlalchemy.orm import Session

from movieapi.constants import SQLITE_DB_FILE
from movieapi.db_tables import create_sql_engine, init_db
from movieapi.models import Movie


def create_db(db_url=SQLITE_DB_FILE) -> None:
    engine = create_sql_engine(url=db_url)
    init_db(engine)


YEAR_RE: re.Pattern = re.compile(r"\((\d{4})\)\s*$")


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
        return [""]

    genres_filtered = [g for g in genres.split("|") if len(g) != 0 and g.lower() != "no genres listed"]
    return genres_filtered


def load_movies_data(session: Session, csv_path: str):
    try:
        with open(csv_path, newline="", encoding="utf-8") as fd:
            reader = csv.DictReader(fd)
            for row in reader:
                movie_id = int(row.get("movieId"))
                title, year = extract_title_and_year(row.get("title"))

                if movie_id is None:
                    continue
                movie = Movie(movie_id, title, year)
                session.add(movie)
                session.flush()

                # genres = row.get("genres")
                # genres_filtered = parse_genres(genres)
                # for name in genres_filtered:
                #     genre = Genre(name)
                #     session.add(genre)
                #     session.flush()
                #     movie.genres.append(genre)
        session.commit()

    except OSError:
        pass


if __name__ == "__main__":
    create_db()
