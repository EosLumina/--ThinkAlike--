FROM python:3.12-slim-bookworm@sha256:21ee6f95a28ba3a9348c55da9dca8c1aefab7323f0937c5f27b6b5d72ddbd424

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Configure apt and install packages
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
  # Install git, process tools, lsb-release (common in install instructions)
  && apt-get -y install git iproute2 procps lsb-release \
  # Install node.js and npm securely using the NodeSource repository
  && apt-get -y install curl gnupg \
  && mkdir -p /etc/apt/keyrings \
  && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
  && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" > /etc/apt/sources.list.d/nodesource.list \
  && apt-get update \
  && apt-get -y install nodejs \
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
