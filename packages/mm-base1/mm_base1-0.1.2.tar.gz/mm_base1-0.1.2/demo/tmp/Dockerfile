# syntax=docker/dockerfile:1
FROM python:3.12.5
WORKDIR /code
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN apt update && apt install -y mc
RUN uv venv /venv
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache --no-dev
COPY src/ ./src



RUN python -m build -w -o /dist && \
    pip install --no-cache-dir /dist/*.whl


FROM python:3.12.5-slim
EXPOSE 3000
ENV PATH="/venv/bin:$PATH"
COPY --from=builder /venv /venv

CMD ["gunicorn", "-b", "0.0.0.0:3000", "--timeout", "999", "--threads", "24", "-k", "uvicorn.workers.UvicornWorker", "app.main:server"]
