from sqlalchemy import (
    Column,
    Engine,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    UniqueConstraint,
    create_engine,
)

from movieapi.constants import SQLITE_DB_FILE

metadata = MetaData()

movies_table = Table(
    "movies",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("movie_id", Integer, unique=True, nullable=False),
    Column("title", String(500), nullable=False),
    Column("year", Integer, nullable=True),
    Column("overview", Text, nullable=True),
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
    Column(
        "movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False
    ),
    Column(
        "genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), nullable=False
    ),
    UniqueConstraint("movie_id", "genre_id", name="uq_movie_genre"),
)

ratings_table = Table(
    "ratings",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, nullable=False),
    Column(
        "movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False
    ),
    Column("rating", Float, nullable=False),
    Column("timestamp", Integer, nullable=False),
)


def create_sql_engine(url: str = SQLITE_DB_FILE) -> Engine:
    engine = create_engine(url, connect_args={"check_same_thread": False})
    return engine


def init_db(engine: Engine):
    metadata.create_all(engine)
