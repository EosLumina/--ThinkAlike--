FROM python:3.10-slim

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Configure apt and install packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    # Install git, process tools, lsb-release (common in install instructions)
    && apt-get -y install git iproute2 procps lsb-release \
    # Install node.js and npm
    && apt-get -y install curl \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    # Install Python dependencies
    && apt-get -y install python3-pip python3-dev \
    # Install additional tools
    && apt-get -y install vim wget \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Install global node packages
RUN npm install -g npm@latest

# Setup Python environment
RUN pip install --upgrade pip \
    && pip install black flake8 pytest isort mypy

# Setup code workspace
WORKDIR /workspace

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog
