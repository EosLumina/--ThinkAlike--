# MVP Implementation Guide

This document outlines the plan for implementing the Minimum Viable Product (MVP) for the ThinkAlike platform. It
defines the core features, technology stack, and a prioritized implementation path, reflecting the project's focus on
fostering meaningful social connections based on shared ideas and values, underpinned by ethical principles and data
transparency.

## Key References

* **Source of Truth:** [Master Reference](../../core/master_reference.md)

* **Manifesto:** [Philosophical Manifesto](../../core/manifesto/manifesto.md)
* **Architectural Design Specs:** [Architectural Design

Specifications](../../architecture/design/architectural_design_specifications.md)

* **API Documentation:** [API Endpoints](../../architecture/api/api_endpoints.md)

* --

## 1. Core Vision (MVP Focus)

The ThinkAlike MVP aims to demonstrate the core concept of connecting users based on the similarity of their "thought
profiles" (represented by interconnected nodes of ideas, values, interests). The focus is on:

* **Building Thought Profiles:** Allowing users to create and connect nodes representing their unique perspectives.

* **Simplified Matching:** Implementing a basic algorithm to identify potential connections based on shared or similar

profile elements.

* **Data Traceability Visualization:** Providing a basic visual representation of how data flows and how matches are

determined.

* **User Control & Ethics:** Ensuring users have control over their profiles and the connection process, adhering to

ethical guidelines.

* --

## 2. MVP Core Features

### User Authentication

* Secure user registration (username, password).

* Secure user login/logout (using JWT or sessions).
* (Future) Password recovery.

### User "Thought Profile" Building

* Users can create, read, update, and delete "Nodes" (representing ideas, values, interests, skills, etc.).

* Nodes will have properties like title, content, and potentially `nodeType` (e.g., 'value', 'interest').
* Users can create and delete "Connections" between their own nodes.

### Basic Matching

* Backend implements a placeholder matching algorithm (e.g., based on counting shared nodes/tags).

* Frontend displays a list of potential user matches based on this simple algorithm.

### Basic Connection Mechanism

* Users can view basic profiles of potential matches.

* Users can send/accept/reject simple connection requests (no complex messaging yet).

### Data Traceability Visualization (DataTraceability.jsx)

* Displays a graph representation of fetched data (initially, this might be a user's own thought profile or a comparison

with a match).

* Includes basic tooltips on hover for nodes and edges.
* (Post-MVP) Will incorporate more advanced visualization of matching rationale, ethical weighting, and user

customization.

* --

## 3. Technology Stack

* **Frontend:** React (Create React App), react-router-dom, react-force-graph-2d (or alternative), react-tooltip.

* **Backend:** Python (FastAPI), Uvicorn, Gunicorn (for deployment).
* **Database:** SQLite (for local development), PostgreSQL (planned for Render production).

* **ORM:** SQLAlchemy.
* **Authentication:** Flask-Login (or equivalent FastAPI mechanism like python-jose for JWT).

* **Deployment:** Render (Backend as Web Service, Frontend as Static Site).
* **Documentation:** Markdown.

* **Testing:** pytest (Backend), React Testing Library (Frontend), Cypress (E2E - Future).

* --

## 4. Implementation Roadmap (Phased)

### Phase 1: Backend Foundation (Highest Priority)

* [ ] **1.1. Database Setup (SQLite + SQLAlchemy):**
  * Create a schema.sql file with essential tables (users, nodes, connections)
  * Implement initial SQLAlchemy models
  * Create database initialization script

* [ ] **1.2. Core API Endpoints:**
  * Implement authentication endpoints (register, login, logout)
  * Create basic CRUD for user profile
  * Implement node creation/retrieval endpoints
  * Add simple matching endpoint

* [ ] **1.3. Basic Verification System:**
  * Create simple validation rules for user input
  * Implement core ethical checks
  * Set up audit logging foundation

### Phase 2: Frontend Essentials

* [ ] **2.1. User Interface Shell:**
  * Implement login/registration screens
  * Create main navigation structure
  * Build profile creation/editing UI

* [ ] **2.2. Node Creation Interface:**
  * Implement the UI for creating and managing nodes
  * Add simple visualization for existing nodes

* [ ] **2.3. Simple Data Traceability:**
  * Create basic version of DataTraceability component
  * Implement simple graph visualization

### Phase 3: Integration & Testing

* [ ] **3.1. Frontend-Backend Integration:**
  * Connect all frontend components to API endpoints
  * Test full user journey (registration → profile → nodes)

* [ ] **3.2. Unit & Integration Tests:**
  * Write basic test suite for critical paths
  * Set up testing framework

### Phase 4: Deployment

* [ ] **4.1. Docker Configuration:**
  * Create Dockerfiles for frontend and backend
  * Set up Docker Compose for local development

* [ ] **4.2. CI/CD Pipeline:**
  * Set up GitHub Actions for automated testing
  * Configure automatic deployment to Render

* [ ] **4.3. Documentation:**
  * Update installation guide
  * Create contributor quick start guide

* --

### Phase 5: Deployment and Testing

* [ ] **5.1. Final Backend Testing (Local):** Ensure all backend endpoints work correctly with the database.

* [ ] **5.2. Final Frontend Testing (Local):** Ensure all frontend components and interactions work correctly locally.
* [ ] **5.3. Build Frontend for Production:**
  * Run `npm run build` inside frontend.
  * Move `frontend/build` to the project root.
* [ ] **5.4. Deploy Backend to Render (Web Service):** Push changes to GitHub. Ensure Render deploys the latest commit.

* [ ] **5.5. Deploy Frontend to Render (Static Site):** Push changes (including the build folder) to GitHub. Ensure

Render Static Site settings are correct (Root Dir blank, Build Command blank, Publish Dir build, environment variable
set). Trigger a manual deploy with cleared cache.

* [ ] **5.6. Update CORS:** Update `main.py` with the final frontend Render URL and redeploy the backend.

* [ ] **5.7. Post-Deployment Testing:** Thoroughly test the entire application on the live Render URLs.

* --

### Phase 6: Documentation & Cleanup

* [ ] **6.1. Update `README.md`:** Add comprehensive setup, run, and deployment instructions.

* [ ] **6.2. Clean up temporary files.
* [ ] **6.3. Remove build folder.

* --

## Document Details

* Title: MVP Implementation Guide

* Type: Technical Documentation

* Version: 1.0.0

## - Last Updated: 2025-04-05

End of MVP Implementation Guide
