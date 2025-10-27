from pathlib import Path

from sqlalchemy import select

from movieapi import models
from scripts.load_data import load_movies_data, load_ratings_data


def test_movie_ingestion(db_session, tmp_movielens: dict[str, Path]):
    csv_path = tmp_movielens.get("MOVIES_CSV")
    expected_genres = {"adventure", "animation", "children", "comedy", "fantasy"}

    load_movies_data(db_session, csv_path)

    movies = db_session.scalars(select(models.Movie).order_by(models.Movie.movie_id)).all()
    assert [m.movie_id for m in movies] == [1, 2, 3, 201, 202, 203, 204]
    assert movies[0].title == "Toy Story"

    toy_story = movies[0]
    toy_genres = {g.name for g in toy_story.genres}
    assert expected_genres <= toy_genres


def test_ratings_ingestion(db_session, tmp_movielens: dict[str, Path]):
    movie_path = tmp_movielens.get("MOVIES_CSV")
    ratings_path = tmp_movielens.get("RATINGS_CSV")
    load_movies_data(db_session, movie_path)

    load_ratings_data(db_session, ratings_path)

    toy = db_session.scalars(select(models.Movie).where(models.Movie.movie_id == 1)).one()
    ratings = db_session.scalars(select(models.Rating).where(models.Rating.movie_id == toy.id)).all()
    assert len(ratings) == 2
