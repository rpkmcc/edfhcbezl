# MovieAPI

# Dev

## Running local 
- pip install -e '.[dev]'
- docker build -t movieapi:latest .
- docker run -d --name movieapi -p 127.0.0.1:8000:8000  movieapi:latest

## Running with compose
- docker compose build
- docker compose up -d
