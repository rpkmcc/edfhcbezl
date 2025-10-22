from pathlib import Path

from sqlalchemy import select

from movieapi import models
from scripts.load_data import load_movies_data


def test_year_title_extraction():
    pass


def test_movie_ingestion(db_session, tmp_movielens: dict[str, Path]):
    csv_path = tmp_movielens.get("MOVIES_CSV")

    load_movies_data(db_session, csv_path)

    movies = db_session.scalars(select(models.Movie).order_by(models.Movie.movie_id)).all()
    assert [m.movie_id for m in movies] == [1, 2, 3]
    assert movies[0].title == "Toy Story"
