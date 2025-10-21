#!/usr/bin/env bash
echo "[ENTYRPOINT] Starting the Movie API server..."

exec /usr/local/bin/gunicorn \
  --workers 2 \
  --pythonpath /workspace/src \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  movieapi.app:app
    