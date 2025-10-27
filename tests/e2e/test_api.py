import pytest
import requests

from movieapi.constants import BASE_URL

pytest.mark.e2e


@pytest.fixture()
def base_url() -> str:
    return f"http://localhost:8000/{BASE_URL}"


def test_happy_path_get_movie_by_id(base_url):
    movie_id = 1

    response = requests.get(f"{base_url}/movies/{movie_id}")
    payload = response.json()

    assert response.status_code == 200
    assert payload.get("title") == "Toy Story"


def test_happy_path_get_movies_by_filter(base_url):
    params = {"q": "recommend action movies above 4.8", "limit": 3}

    response = requests.get(f"{base_url}/movies/search", params=params)
    payload = response.json()

    assert response.status_code == 200
    assert len(payload.get("results")) == 3

    for movie in payload.get("results"):
        genres = movie.get("genres")
        assert "action" in genres
