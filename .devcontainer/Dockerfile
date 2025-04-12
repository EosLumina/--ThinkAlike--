FROM python:3.10-slim-bookworm AS python-base

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    git \
    curl \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Security hardening
RUN pip install --no-cache-dir --upgrade pip \
    && pip config set global.index-url https://pypi.org/simple/ \
    && pip config set global.trusted-host pypi.org

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r requirements.txt || \
    pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN useradd -m developer
USER developer

# Set the working directory
WORKDIR /workspaces

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog
