from fastapi import FastAPI, status
from sqlalchemy.orm import Session, sessionmaker

from movieapi.constants import BASE_URL
from movieapi.db_tables import create_sql_engine

# from movieapi.routers import movies

session: sessionmaker[Session] = sessionmaker(bind=create_sql_engine())
app = FastAPI()
# app.include_router(movies.router)


@app.get(f"{BASE_URL}", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}
