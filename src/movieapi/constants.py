from pathlib import Path

API_VERSION: str = "v1"
BASE_URL: str = f"/api/{API_VERSION}"
JSON_MEDIA_TYPE: str = "application/json"
DATA_DIR: str = "/workspace/data"
SQLITE_DB_FILE: str = f"sqlite:///{DATA_DIR}/movieapi.db"
MOVIES_CSV_PATH: str = Path("/workspace/dataset/movies.csv")
RATINGS_CSV_PATH: str = Path("/workspace/dataset/ratings.csv")
