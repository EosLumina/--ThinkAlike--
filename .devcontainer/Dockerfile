FROM python:3.11-slim-bullseye AS python-base

# Install dependencies for development environment
RUN apk add --no-cache \
    git \
    curl \
    nodejs \
    npm \
    # Add additional security packages
    ca-certificates \
    # Add build dependencies
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    postgresql-dev \
    # Shell for development experience
    bash

# Security hardening
RUN pip install --no-cache-dir --upgrade pip \
    && pip config set global.index-url https://pypi.org/simple/ \
    && pip config set global.trusted-host pypi.org \
    && pip install pip-audit

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN addgroup -S developer && adduser -S developer -G developer -s /bin/bash
USER developer

# Set the working directory
WORKDIR /workspaces
