// filepath: C:\--ThinkAlike--\docs\guides\implementation_guides\mvp_implementation_guide.md
# Mvp Implementation Guide

# MVP Implementation Guide

This document outlines the plan for implementing the Minimum Viable Product (MVP) for the ThinkAlike platform. It defines the core features, technology stack, and a prioritized implementation path, reflecting the project's focus on fostering meaningful social connections based on shared ideas and values, underpinned by ethical principles and data transparency.

Reference: This guide builds upon and clarifies information found in the SOURCE OF TRUTH - THINKALIKE PROJECT - MASTER REFERENCE.md. Always refer to the Source of Truth for the definitive project vision and specifications.

1. Core Vision (MVP Focus)
The ThinkAlike MVP aims to demonstrate the core concept of connecting users based on the similarity of their "thought profiles" (represented by interconnected nodes of ideas, values, interests). The focus is on:

Building Thought Profiles: Allowing users to create and connect nodes representing their unique perspectives.
Simplified Matching: Implementing a basic algorithm to identify potential connections based on shared or similar profile elements.
Data Traceability Visualization: Providing a basic visual representation of how data flows and how matches are determined.
User Control & Ethics: Ensuring users have control over their profiles and the connection process, adhering to ethical guidelines.
2. MVP Core Features
User Authentication:
Secure user registration (username, password).
Secure user login/logout (using JWT or sessions).
(Future) Password recovery.
User "Thought Profile" Building:
Users can create, read, update, and delete "Nodes" (representing ideas, values, interests, skills, etc.).
Nodes will have properties like title, content, and potentially nodeType (e.g., 'value', 'interest').
Users can create and delete "Connections" between their own nodes.
Basic Matching:
Backend implements a placeholder matching algorithm (e.g., based on counting shared nodes/tags).
Frontend displays a list of potential user matches based on this simple algorithm.
Basic Connection Mechanism:
Users can view basic profiles of potential matches.
Users can send/accept/reject simple connection requests (no complex messaging yet).
Data Traceability Visualization (DataTraceability.jsx):
Displays a graph representation of fetched data (initially, this might be a user's own thought profile or a comparison with a match).
Includes basic tooltips on hover for nodes and edges.
(Post-MVP) Will incorporate more advanced visualization of matching rationale, ethical weighting, and user customization.
Explicitly Excluded from MVP:

Complex AI/NLP-based matching algorithms.
Advanced visualization features (pulsing, waveforms, complex animations).
Community features (Mode 3).
Real-time messaging or chat.
Detailed profile customization beyond nodes/connections.
Advanced search/filtering.
3. Technology Stack
Frontend: React (Create React App), react-router-dom, react-force-graph-2d (or alternative), react-tooltip.
Backend: Python (FastAPI), Uvicorn, Gunicorn (for deployment).
Database: SQLite (for local development), PostgreSQL (planned for Render production).
ORM: SQLAlchemy.
Authentication: Flask-Login (or equivalent FastAPI mechanism like python-jose for JWT).
Deployment: Render (Backend as Web Service, Frontend as Static Site).
Documentation: Markdown.
Testing: pytest (Backend), React Testing Library (Frontend), Cypress (E2E - Future).
4. Implementation Roadmap (Phased)
Phase 1: Backend Foundation (Highest Priority)

[ ] 1.1. Database Setup (SQLite + SQLAlchemy):
Finalize schema.sql for users (with hashed passwords), nodes (with user_id), and connections tables.
Implement SQLAlchemy models (app/models.py).
Set up database initialization (app/__init__.py).
[ ] 1.2. Implement User Authentication:
Add Flask-Login (or JWT equivalent) to the backend.
Create routes for /register, /login, /logout.
Implement password hashing (werkzeug.security).
Protect relevant API endpoints using @login_required (or JWT decorator).
[ ] 1.3. Implement Node & Connection CRUD (using DB):
Convert all existing API endpoints (/api/nodes, /api/nodes/<id>, /api/connections, /api/connections/<id>) to use SQLAlchemy to interact with the SQLite database.
Ensure all endpoints are associated with the logged-in user (current_user).
Implement robust error handling and input validation for all endpoints.
[ ] 1.4. Basic /api/match Endpoint:
Create a placeholder /api/match endpoint that simply returns a list of all users except the current user (no actual matching logic yet).
Phase 2: Frontend Core UI & Local Integration

[ ] 2.1. Refactor Frontend Component: Rename Notes.js to Nodes.js (or ProfileBuilder.js). Adapt App.js import.
[ ] 2.2. Implement Node CRUD UI (Nodes.js/ProfileBuilder.js):
Connect the existing UI elements (inputs, buttons) to the backend API endpoints for creating, reading, updating, and deleting nodes.
Fetch and display the logged-in user's nodes.
[ ] 2.3. Basic UserProfile.js: Create a component to display basic user info (fetched from a new /api/users/<id> endpoint on the backend).
[ ] 2.4. Basic UserDiscovery.js: Create a component that fetches data from the placeholder /api/match endpoint and displays a simple list of usernames.
[ ] 2.5. Frontend Routing (App.js): Ensure App.js includes routes for UserProfile.js and UserDiscovery.js.
[ ] 2.6. Local Testing: Test all Node CRUD operations and the basic user discovery flow locally using npm start (frontend) and python -m uvicorn main:app --reload (backend).
Phase 3: Basic Connection Mechanism

[ ] 3.1. Connection Request API (Backend): Add endpoints to handle sending, accepting, and rejecting connection requests (e.g., POST /api/connections/requests, PUT /api/connections/requests/<request_id>). Update the database schema if necessary.
[ ] 3.2. Connection Request UI (Frontend): Add buttons/UI elements in UserDiscovery.js or UserProfile.js to send connection requests. Add a section to display pending requests and allow accepting/rejecting.
Phase 4: DataTraceability Visualization (Refined)

[ ] 4.1. Integrate Real Data: Modify DataTraceability.jsx to fetch and display relevant graph data based on the current context (e.g., the user's own profile, or a visualization comparing the user to a potential match fetched via /api/match). Remove placeholder data/logic.
[ ] 4.2. Basic Styling: Apply the "Cyberpunk Data Stream" styling basics (colors, fonts) to the graph nodes and edges.
[ ] 4.3. Working Tooltips: Ensure tooltips function correctly using react-force-graph-2d's built-in mechanisms (nodeLabel, linkLabel).
Phase 5: Deployment and Testing

[ ] 5.1. Final Backend Testing (Local): Ensure all backend endpoints work correctly with the database.
[ ] 5.2. Final Frontend Testing (Local): Ensure all frontend components and interactions work correctly locally.
[ ] 5.3. Build Frontend for Production:
Run npm run build inside frontend.
Move frontend/build to the project root.
[ ] 5.4. Deploy Backend to Render (Web Service): Push changes to GitHub. Ensure Render deploys the latest commit.
[ ] 5.5. Deploy Frontend to Render (Static Site): Push changes (including the build folder) to GitHub. Ensure Render Static Site settings are correct (Root Dir blank, Build Command blank, Publish Dir build, environment variable set). Trigger a manual deploy with cleared cache.
[ ] 5.6. Update CORS: Update main.py with the final frontend Render URL and redeploy the backend.
[ ] 5.7. Post-Deployment Testing: Thoroughly test the entire application on the live Render URLs.
Phase 6: Documentation & Cleanup

[ ] 6.1. Update README.md: Add comprehensive setup, run, and deployment instructions.
[ ] 6.2. Clean up temporary files.
[ ] 6.3. Remove build folder.
Ongoing:

Implement basic testing (pytest, React Testing Library).
Refine styling and UI/UX.
Improve matching algorithm.
Address security vulnerabilities (npm audit).
Add more comprehensive documentation.
[ ] 6.4. Implement more complex matching algorithm.

---
**Document Details**
- Title: Mvp Implementation Guide
- Type: Technical Documentation
- Version: 1.0.0
- Last Updated: 2025-04-05
---
End of Mvp Implementation Guide
---



