from fastapi import FastAPI, status

from movieapi.constants import BASE_URL

# from movieapi.routers import movies

app = FastAPI()
# app.include_router(movies.router)


@app.get(f"{BASE_URL}", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}
