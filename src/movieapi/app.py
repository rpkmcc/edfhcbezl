from fastapi import FastAPI, status

from movieapi.constants import API_VERSION, BASE_URL, JSON_MEDIA_TYPE

app = FastAPI()


@app.get(f"{BASE_URL}", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}
