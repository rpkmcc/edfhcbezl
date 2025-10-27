import re

from sqlalchemy import func, literal, select
from sqlalchemy.orm import Session

from movieapi.db_tables import movie_genres_table
from movieapi.models import Genre, Movie, Rating

YEAR_RE = re.compile(r"\b(19\d{2}|20\d{2})\b")
RATING_RE = re.compile(r"(?:rating\s*[>]\s*|above\s*|over\s*)(\d+(?:\.\d+)?)")


def get_movie(movie_id: int, session: Session) -> Movie | None:
    try:
        movie = session.scalars(select(Movie).where(Movie.movie_id == movie_id)).first()
        return movie
    except Exception as er:
        print(f"{er}")


def get_genres(session: Session) -> list[Genre]:
    try:
        names = session.scalars(select(Genre.name)).all()
        return [name.lower() for name in names if name]
    except Exception as er:
        print(f"{er}")


def detect_genre(query: str, genres: list[str]) -> str | None:
    for genre in genres:
        if genre in query:
            return genre
    return None


def parse_movies_query(text: str, genres: list[str]) -> dict:
    query = text.lower().strip()
    recommend = any(word in query for word in ("recommend", "suggest", "top", "best"))

    match_year = YEAR_RE.search(query)
    year = int(match_year.group(1)) if match_year else None

    match_rating = RATING_RE.search(query)
    rating = float(match_rating.group(1)) if match_rating else None

    genre = detect_genre(query, genres)

    intent = "recommend" if recommend else "unknown"
    return {"intent": intent, "genre": genre, "year": year, "title": None, "rating": rating}


def get_movies(session: Session, query: str, limit=10) -> dict:
    genres = get_genres(session)
    parsed = parse_movies_query(query, genres)
    wanted_genre = parsed.get("genre")  # e.g. "drama" (already lowercase)
    wanted_year = parsed.get("year")  # e.g. 1999 or None
    rating = parsed.get("rating")  # e.g. 4.0 or None
    recommend = parsed.get("intent")

    # One row per movie: (movie_id, avg_rating)
    avg_rating = (
        select(Rating.movie_id.label("movie_id"), func.avg(Rating.rating).label("avg_rating"))
        .group_by(Rating.movie_id)
        .subquery()
    )

    # Base query: Movie + its avg_rating (if any)
    stmt = select(Movie, avg_rating.c.avg_rating).outerjoin(avg_rating, avg_rating.c.movie_id == Movie.id)

    # Apply Filters
    if wanted_genre is not None:
        stmt = (
            stmt.join(movie_genres_table, movie_genres_table.c.movie_id == Movie.id)
            .join(Genre, Genre.id == movie_genres_table.c.genre_id)
            .where(func.lower(Genre.name) == wanted_genre)
        )

    if wanted_year is not None:
        stmt = stmt.where(Movie.year == wanted_year)

    if rating is not None:
        stmt = stmt.where(avg_rating.c.avg_rating >= rating)

    # Ordering
    if recommend == "recommend":
        stmt = stmt.order_by(func.coalesce(avg_rating.c.avg_rating, literal(0)).desc(), Movie.id.asc())
    else:
        stmt = stmt.order_by(Movie.id.asc())

    stmt = stmt.limit(limit)

    rows = session.execute(stmt).all()
    results = []
    for movie, avg_rating in rows:
        results.append(
            {
                "movie_id": movie.movie_id,
                "title": movie.title,
                "year": movie.year,
                "genres": [g.name for g in movie.genres],
                "rating": round(float(avg_rating), 2) if avg_rating is not None else None,
            }
        )
    return {"parsed": parsed, "results": results}
