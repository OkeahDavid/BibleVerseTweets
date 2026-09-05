# Verse-of-the-day bot -- always-on worker image.
# Same shape as fpl-bot / forex-signal-bot: official Python base + uv binary copied in.
FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.8.5 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Dependencies first for layer caching.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

# posted_verses.log lives here. Mount a Railway Volume at /data for persistence
# (Railway rejects the Dockerfile VOLUME instruction, so it's set in the dashboard).
ENV DATA_DIR=/data

# Runs both the daily post schedule and the interactive /verse listener.
CMD ["uv", "run", "--frozen", "scheduler.py"]
