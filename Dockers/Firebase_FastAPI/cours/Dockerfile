FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv /uv /uvx /bin/

ADD . /app/cours

# Set workdir
WORKDIR /app/cours

# Install dependencies
RUN uv sync --locked

# Expose port
EXPOSE 7000

# Run app
CMD ["uv","run","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
