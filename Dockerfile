FROM python:3.11-slim

WORKDIR /workspace
ENV PYTHONPATH=/workspace/src

ENV DB_PATH=/workspace/data/movieapi.db

COPY pyproject.toml entrypoint.sh ./
COPY scripts ./scripts
COPY src ./src

RUN pip install gunicorn && \
    pip install --no-cache-dir . && \
    apt-get update && apt-get install -y --no-install-recommends vim procps sqlite3 && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENTRYPOINT ["/workspace/entrypoint.sh"]
# ENTRYPOINT [ "tail", "-f", "/dev/null" ]