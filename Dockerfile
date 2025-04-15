# Use Python Alpine as base image - zero vulnerabilities
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Create a non-root user for running the application
RUN addgroup -S thinkalike && adduser -S thinkalike -G thinkalike \
    && mkdir -p /home/thinkalike \
    && chown -R thinkalike:thinkalike /home/thinkalike \
    && chown -R thinkalike:thinkalike /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies required for some Python packages
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    postgresql-dev

# Copy the requirements file into the container
COPY backend/requirements.txt .

# Install the dependencies with security best practices
RUN pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps \
    && rm -rf /tmp/*

# Copy the rest of the application code
COPY backend /app/backend
COPY frontend /app/frontend

# Set proper permissions
RUN chown -R thinkalike:thinkalike /app

# Switch to non-root user
USER thinkalike

# Expose the port the app runs on
EXPOSE 8000

# Command to run the backend server
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
