import pytest

from movieapi.services import get_movie, get_movies
from scripts.load_data import load_movies_data, load_ratings_data


@pytest.fixture()
def seed_db(db_session, tmp_movielens):
    load_movies_data(db_session, tmp_movielens.get("MOVIES_CSV"))
    load_ratings_data(db_session, tmp_movielens.get("RATINGS_CSV"))
    return db_session


def test_get_movie_by_id(seed_db):
    expected_result = ["adventure", "animation", "children", "comedy", "fantasy"]

    movie = get_movie(movie_id=1, session=seed_db)

    assert movie.movie_id == 1
    assert movie.title == "Toy Story"
    assert movie.year == 1995
    assert [g.name for g in movie.genres] == expected_result


def test_movies_from_1995_unknown_intent(seed_db):
    result = get_movies(seed_db, "movies from 1995")

    titles = {r["title"] for r in result["results"]}
    assert {"Toy Story", "Jumanji", "Grumpier Old Men"} <= titles


@pytest.mark.parametrize(
    "query, expected_first",
    [
        ("recommend movies from 2010", "Inception"),
        ("recommend movies from 2008", "The Dark Knight"),
        ("recommend movies from 2000", "Gladiator"),
    ],
)
def test_recommend_orders_by_avg_rating(seed_db, query, expected_first):
    result = get_movies(seed_db, query)

    assert result["parsed"]["intent"] == "recommend"
    assert len(result["results"]) >= 1
    assert result["results"][0]["title"] == expected_first


@pytest.mark.parametrize(
    "query, expected_titles_subset",
    [
        ("recommend movies above 4.8", {"The Dark Knight"}),  # 4.9/4.8 avg ≈ 4.85
        ("recommend movies above 4.6", {"The Dark Knight", "Inception", "Gladiator"}),  # ≈4.85, 4.75, 4.65
        (
            "movies above 4.2",
            {"The Hangover", "The Dark Knight", "Inception", "Gladiator"},
        ),  # unknown intent still filters
    ],
)
def test_rating_filter(seed_db, query, expected_titles_subset):
    result = get_movies(seed_db, query)
    titles = {r["title"] for r in result["results"]}

    # Ensure all expected are present
    assert expected_titles_subset <= titles


def test_limit_is_enforced(seed_db):
    result = get_movies(seed_db, "recommend movies", limit=3)

    assert len(result["results"]) == 3
