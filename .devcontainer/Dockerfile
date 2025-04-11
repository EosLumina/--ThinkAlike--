FROM python:3.10.13-slim-bullseye@sha256:c623b7c1ffa10ca3fca5a3a9addfb51fde20f5ad8e687ca1ed3f0d8d4ac83083

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Configure apt and install packages
RUN apt-get update \
  && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
  # Install git, process tools, lsb-release (common in install instructions)
  && apt-get -y install git iproute2 procps lsb-release \
  # Install node.js and npm securely using the NodeSource repository
  && apt-get -y install curl gnupg \
  && mkdir -p /etc/apt/keyrings \
  && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
  && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_16.x nodistro main" > /etc/apt/sources.list.d/nodesource.list \
  && apt-get update \
  && apt-get -y install nodejs \
  # Install Python dependencies
  && apt-get -y install python3-pip python3-dev \
  # Install additional tools
  && apt-get -y install vim wget \
  # Security updates
  && apt-get upgrade -y \
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
