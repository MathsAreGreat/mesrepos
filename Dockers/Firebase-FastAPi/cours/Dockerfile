FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app/cours

# Set the working directory
WORKDIR /app/cours

RUN uv sync --locked

# Expose port 7000
EXPOSE 7000

# Run the application
CMD ["uv","run","uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]