# Collaborative Development Hub (Presence & Communication) Specification

## Purpose
Visualize project progress, show who’s working on what, and enable direct, contextual communication between contributors in real time.

## Features
* Real-time contributor presence (opt-in)
* Live roadmap visualization with avatars on active nodes
* Clickable nodes for chat, swarm join, or async message
* Integration with VSCode extension for presence/status
* In-app chat, ping, or video call (optional)
* Privacy controls for all presence features

## API & Data Model
* WebSocket API for presence updates (`/api/presence`)
* Contributor activity logging (opt-in)
* Data model: `UserPresence`, `ActiveTask`, `Message`

## UI/UX Notes
* Roadmap (D3.js/React) with live avatars
* Contributors can see who is online and what they’re working on
* Direct communication via chat or ping from roadmap nodes
* Presence is always opt-in and can be toggled

## Security/Ethics
* All presence and activity sharing is opt-in
* No surveillance or forced tracking
* All communication is encrypted and private by default

## Example User Flow
1. Contributor logs in and opts in to presence
2. Their avatar appears on the roadmap at their active task
3. Another contributor clicks their avatar to open a chat or send a ping
4. Contributors can form swarms or join tasks in real time

---
*End of Collaborative Development Hub Spec*