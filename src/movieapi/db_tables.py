from sqlalchemy import (
    CheckConstraint,
    Column,
    Engine,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import registry, relationship

from movieapi import models
from movieapi.constants import SQLITE_DB_FILE

mapper_registry = registry()

metadata = mapper_registry.metadata

movies_table = Table(
    "movies",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("movie_id", Integer, unique=True, nullable=False),
    Column("title", String(500), nullable=False),
    Column("year", Integer, nullable=True),
)

genres_table = Table(
    "genres",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), unique=True, nullable=False),
)

movie_genres_table = Table(
    "movie_genres",
    metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

ratings_table = Table(
    "ratings",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, nullable=False),
    Column("movie_id", Integer, ForeignKey("movies.id"), nullable=False),
    Column("rating", Float, CheckConstraint("rating >= 0.5 AND rating <= 5.0"), nullable=False),
    Column("timestamp", Integer, nullable=False),
)


def start_mappers() -> None:
    ## Movie <-> movies_table
    mapper_registry.map_imperatively(
        models.Movie,
        movies_table,
        properties={
            "genres": relationship("Genre", secondary=movie_genres_table, back_populates="movies"),
            "ratings": relationship("Rating"),
        },
    )

    # Genre <-> genres_table
    mapper_registry.map_imperatively(
        models.Genre,
        genres_table,
        properties={
            "movies": relationship("Movie", secondary=movie_genres_table, back_populates="genres"),
        },
    )

    # Rating <-> ratings_table
    mapper_registry.map_imperatively(
        models.Rating,
        ratings_table,
        properties={
            "movie": relationship(models.Movie, back_populates="ratings"),
        },
    )


def create_sql_engine(url: str = SQLITE_DB_FILE) -> Engine:
    engine = create_engine(url, connect_args={"check_same_thread": False})
    return engine


def init_db(engine: Engine):
    metadata.create_all(engine)
