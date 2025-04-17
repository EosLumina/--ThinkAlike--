# Use the latest secure Python 3.10 version
FROM mcr.microsoft.com/devcontainers/python:3.10

# Install additional dependencies for development environment
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    git \
    curl \
    nodejs \
    npm \
    # Add additional security packages
    ca-certificates \
    # Add build dependencies
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Security hardening
RUN pip install --no-cache-dir --upgrade pip \
    && pip config set global.index-url https://pypi.org/simple/ \
    && pip config set global.trusted-host pypi.org \
    && pip install pip-audit

# Set the working directory in the container
WORKDIR /workspaces

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
