# AI Onboarding Agent Specification

## Purpose
A friendly, context-aware AI agent greets users on project start (terminal or web), explains ThinkAlike’s vision, guides onboarding, and answers questions.

## Features
* Greets user on first run (terminal and/or web UI)
* Explains project vision, values, and how to get started
* Offers guided tour of documentation and contribution process
* Answers basic questions about the project, architecture, and contribution
* Optionally, provides links to live docs, community, and support

## API & Data Model
* `GET /api/onboarding/intro` – Returns greeting and intro text
* `POST /api/onboarding/ask` – Accepts user question, returns answer
* Configurable agent persona (Eos Lumina∴ or custom)

## UI/UX Notes
* Terminal: Print greeting and onboarding steps on `manage.py run` or first CLI use
* Web: Modal or welcome screen on first login/visit
* Option to skip or revisit onboarding at any time

## Security/Ethics
* No tracking or analytics by default
* All onboarding content is open and auditable

## Example User Flow
1. User runs `python manage.py run` or opens web app
2. AI agent greets: “Welcome to ThinkAlike! I’m Eos Lumina∴, your guide...”
3. Agent offers: “Would you like a tour, to read the manifesto, or to start building?”
4. User can ask questions or follow guided steps

---
*End of AI Onboarding Agent Spec*