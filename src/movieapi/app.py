from fastapi import FastAPI, status

from movieapi.constants import BASE_URL
from movieapi.db_tables import start_mappers
from movieapi.routers import chat, movies

start_mappers()
app = FastAPI()
app.include_router(movies.router)
app.include_router(chat.router)


@app.get(f"{BASE_URL}", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}
