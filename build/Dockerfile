# Use a more recent Python version
FROM python:3.12-alpine AS build

# Install Poetry
RUN apk add --no-cache curl \
    && curl -sSL https://install.python-poetry.org | python3 -

# Set up environment
ENV POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy and install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-ansi --no-interaction \
    && poetry export -f requirements.txt -o requirements.txt

# Final stage
FROM python:3.12-alpine AS final

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY --from=build /app/requirements.txt ./
RUN apk add --no-cache \
    su-exec \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --upgrade pip \
    && rm -rf /root/.cache \
    && rm /app/requirements.txt

# Copy application code
COPY main.py .

# Create non-root user
RUN addgroup -g 1001 -S appgroup \
    && adduser -u 1001 -S -D -G appgroup appuser

# Set permissions
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser
EXPOSE 8000
# Start application
CMD ["python", "main.py"]
