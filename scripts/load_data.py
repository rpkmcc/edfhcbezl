from movieapi.constants import SQLITE_DB_FILE
from movieapi.db_tables import create_sql_engine, init_db


def create_db(db_url=SQLITE_DB_FILE) -> None:
    engine = create_sql_engine(url=db_url)
    init_db(engine)


def load_data():
    pass


if __name__ == "__main__":
    create_db()
