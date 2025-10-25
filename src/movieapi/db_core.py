from typing import Generator

from sqlalchemy.orm import Session, sessionmaker

from movieapi.db_tables import create_sql_engine

Sess: sessionmaker[Session] = sessionmaker(bind=create_sql_engine())


def get_session() -> Generator[Session, None, None]:
    db_session = Sess()
    try:
        yield db_session
    finally:
        db_session.close()
