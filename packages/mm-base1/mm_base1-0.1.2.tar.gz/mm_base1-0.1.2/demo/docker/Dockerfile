# syntax=docker/dockerfile:1.3
FROM python:3.12.5 AS builder

COPY --from=ghcr.io/astral-sh/uv:0.4.3 /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.12

# Create a virtual environment
RUN --mount=type=cache,target=/root/.cache \
    set -ex \
    && uv venv /app/.venv

# Install dependencies
COPY pyproject.toml uv.lock /app/
RUN --mount=type=cache,target=/root/.cache \
    set -ex \
    && cd /app \
    && uv sync --frozen --no-install-project --no-dev

# Build the project
COPY src/ pyproject.toml uv.lock /code/
RUN --mount=type=cache,target=/root/.cache/uv uvx --from build pyproject-build --installer uv -w -o /dist /code

# Install the project package
RUN --mount=type=cache,target=/root/.cache \
    set -ex \
    && uv pip install --python=/app/.venv --no-deps /dist/*.whl


FROM python:3.12.5-slim
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 3000

COPY --from=builder --chown=app:app /app/.venv /app/.venv

RUN set -ex \
    && groupadd -r app \
    && useradd -r -d /app -g app -N app \
    && mkdir /data \
    && chown -R app:app /data
USER app


CMD ["gunicorn", "-b", "0.0.0.0:3000", "--timeout", "999", "--threads", "24", "-k", "uvicorn.workers.UvicornWorker", "app.main:server"]
