import pytest

from movieapi.services import get_movie
from scripts.load_data import load_movies_data, load_ratings_data


@pytest.fixture()
def seed_db(db_session, tmp_movielens):
    load_movies_data(db_session, tmp_movielens.get("MOVIES_CSV"))
    load_ratings_data(db_session, tmp_movielens.get("RATINGS_CSV"))
    return db_session


def test_get_movie_by_id(seed_db):
    movie = get_movie(movie_id=1, session=seed_db)

    assert movie.movie_id == 1
    assert movie.title == "Toy Story"
    assert movie.year == 1995
    assert [g.name for g in movie.genres] == ["adventure", "animation", "children", "comedy", "fantasy"]
