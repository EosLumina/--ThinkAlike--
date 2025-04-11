# ThinkAlike AI Onboarding Guide

This tool provides an interactive, AI-guided onboarding experience for new contributors to ThinkAlike, walking them through the project's vision, ethical principles, and contribution process.

## Features

* **Interactive Dialogue**: Simulates a conversation with an AI guide
* **Project Introduction**: Explains ThinkAlike's vision and mission
* **Manifesto Presentation**: Shares key points from the ThinkAlike manifesto
* **Contribution Process**: Walks through how to contribute effectively
* **Contributor Agreement**: Facilitates review and acceptance of the contributor pledge
* **Documentation Access**: Opens relevant documentation for deeper reading
* **Contributor Registration**: Records contributor information and agreement status

## Usage

### Running the Guide

To start the AI onboarding process:

```bash
# From the project root:
python tools/ai_onboarding/ai_guide.py

# Or if you've made it executable:
./tools/ai_onboarding/ai_guide.py
```

### Integration Options

#### 1. GitHub Workflow Integration

Add to your GitHub workflow to automatically suggest the onboarding process for first-time contributors:

```yaml
# In .github/workflows/welcome-contributor.yml
name: Welcome New Contributors
on:
  pull_request_target:
    types: [opened]
jobs:
  welcome:
    runs-on: ubuntu-latest
    if: github.event.pull_request.author_association == 'FIRST_TIME_CONTRIBUTOR'
    steps:
      - uses: actions/checkout@v2
      - name: Welcome Message
        uses: peter-evans/create-or-update-comment@v1
        with:
          issue-number: ${{ github.event.pull_request.number }}
          body: |
            👋 Welcome to ThinkAlike! 
            
            Thank you for your contribution! We recommend going through our interactive AI onboarding process to better understand the project vision and contribution guidelines:
            
            ```
            git clone https://github.com/EosLumina/--ThinkAlike--.git
            cd --ThinkAlike--
            python tools/ai_onboarding/ai_guide.py
            ```
            
            This will help ensure your contributions align with our project's ethical guidelines and technical standards.
