# tests/conftest.py
import csv
from pathlib import Path
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from movieapi.db_tables import init_db, start_mappers


@pytest.fixture(scope="session")
def engine():
    """
    Use a single in-memory SQLite database shared across connections.
    StaticPool + check_same_thread=False keeps the same memory DB for all connections.
    """
    eng = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Start classical mappings and create tables
    start_mappers()
    init_db(eng)
    return eng


@pytest.fixture()
def db_session(engine) -> Generator[Session, None, None]:
    """
    Fresh ORM Session per test. Uses a transaction that rolls back after each test,
    keeping the schema but clearing rows.
    """
    connection = engine.connect()
    trans = connection.begin()
    session = Session(bind=connection, future=True)

    yield session

    session.close()
    trans.rollback()
    connection.close()


@pytest.fixture()
def tmp_movielens(tmp_path: Path) -> dict[str, Path]:
    """
    Create tiny CSV files under a temp directory for movies & ratings.
    Returns a dict with paths to use in tests.
    """

    movies = [
        {"movieId": "1", "title": "Toy Story (1995)", "genres": "Adventure|Animation|Children|Comedy|Fantasy"},
        {"movieId": "2", "title": "Jumanji (1995)", "genres": "Adventure|Children|Fantasy"},
        {"movieId": "3", "title": "Grumpier Old Men (1995)", "genres": "Comedy|Romance"},
    ]
    ratings = [
        {"userId": "10", "movieId": "1", "rating": "4.5", "timestamp": "1112486027"},
        {"userId": "11", "movieId": "1", "rating": "5.0", "timestamp": "1112484676"},
        {"userId": "12", "movieId": "2", "rating": "3.0", "timestamp": "1112484819"},
    ]

    movies_csv = tmp_path / "movies.csv"
    ratings_csv = tmp_path / "ratings.csv"

    with movies_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["movieId", "title", "genres"])
        w.writeheader()
        w.writerows(movies)

    with ratings_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["userId", "movieId", "rating", "timestamp"])
        w.writeheader()
        w.writerows(ratings)

    return {"MOVIES_CSV": movies_csv, "RATINGS_CSV": ratings_csv}
