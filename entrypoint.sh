#!/usr/bin/env bash
set -euo pipefail

mkdir -p /data
echo "DB path - ${DB_PATH}"

if [ -f "${DB_PATH}" ] && \
  sqlite3 "${DB_PATH}" "SELECT EXISTS(SELECT 1 FROM movies);" | grep -q 1; then
  echo " Database already populated — skipping seed."
else
  echo "Seeding database with MovieLen"
  python3.11 /workspace/scripts/load_data.py
  echo "Seed complete."
fi

echo "[ENTYRPOINT] Starting the Movie API server..."

exec /usr/local/bin/gunicorn \
  --workers 2 \
  --pythonpath /workspace/src \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  movieapi.app:app
    