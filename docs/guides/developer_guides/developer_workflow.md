// filepath: C:\--ThinkAlike--\docs\guides\developer_guides\developer_workflow.md
# Developer Workflow Guide

This guide provides a practical, step-by-step workflow for common development tasks within the ThinkAlike project. It integrates information from various guides like [`contributing.md`](../../core/contributing.md), [`installation.md`](../../core/installation.md), style guides, and testing procedures.

**Prerequisites:**

1.  **Environment Setup:** Ensure you have successfully completed the [`Installation Guide`](../../core/installation.md).
2.  **Understanding:** Familiarize yourself with the [`Onboarding Guide`](../../core/onboarding_guide.md), [`Architectural Overview`](../../architecture/architectural_overview.md), and especially the [`Core Concepts Explained`](../../vision/core_concepts.md) (including UI as Validation).
3.  **Issue Tracking:** Have access to the project's GitHub issue tracker [Link - **TODO**].

## General Workflow Steps

1.  **Pick an Issue:** Find an issue to work on from the issue tracker (see [`contributing.md`](../../core/contributing.md) for guidance on finding issues). Assign it to yourself or comment your intention to work on it.
2.  **Create a Branch:** Based on the `main` branch (or `develop` if used), create a new branch following the naming convention: `type/issue-number-short-description` (e.g., `feat/215-add-profile-tagging`).
    ```bash
    git checkout main
    git pull upstream main # Ensure main is up-to-date
    git checkout -b feat/215-add-profile-tagging
    ```
3.  **Develop & Test (Iterative):** This is the core loop. See specific task workflows below.
    * Write code (adhering to [`Code Style Guide`](./code_style_guide.md)).
    * Write unit/integration tests.
    * Run tests locally.
    * Utilize UI Validation components for real-time feedback (see [`UI Validation Examples`](./ui_validation_examples.md)).
    * Document code changes ([`Code Docs Template`](../../templates/code_documentation_template.md)).
4.  **Commit Changes:** Use Conventional Commit messages (e.g., `feat: add tagging feature to user profiles`). Commit frequently with meaningful messages.
5.  **Update Branch:** Regularly rebase or merge `main` into your branch to stay updated: `git fetch upstream && git rebase upstream/main`. Resolve conflicts locally.
6.  **Run All Checks:** Before pushing, ensure all tests pass and linters/formatters succeed:
    ```bash
    # Example commands (adjust based on project setup)
    cd backend && pytest && cd ..
    cd frontend && npm test && npm run lint && npm run format && cd ..
    ```
7.  **Push Branch:** `git push origin feat/215-add-profile-tagging`
8.  **Open Pull Request (PR):** Create a PR on GitHub against the `main` branch. Fill out the PR template, link the issue, and describe your changes.
9.  **Code Review & Iteration:** Respond to reviewer feedback, push additional commits to the *same branch* to address comments.
10. **Merge:** Once approved and checks pass, a maintainer will merge your PR.

## Specific Task Workflows

### Workflow A: Adding a New Backend API Endpoint

1.  **Define Contract:** Define the endpoint path, HTTP method, request body/params (using Pydantic models), and response body (using Pydantic models) – document this briefly in the relevant API doc (e.g., [`api_endpoints_mode2.md`](../../architecture/api/api_endpoints_mode2.md)).
2.  **Create Route:** Add the new endpoint function within the appropriate FastAPI router file in `backend/routes/` (or `api/` if structured differently). Use dependency injection for services. See [`Building Backend Endpoint Guide`](./building_backend_endpoint.md).
3.  **Implement Service Logic:** Create or update a service function in `backend/services/` to handle the business logic for the endpoint. This layer interacts with models/database.
4.  **Database Interaction (if needed):** If data access is required, interact with SQLAlchemy models defined in `backend/models/`. Ensure efficient querying.
5.  **Verification System Hook (if needed):** If the action requires ethical or functional validation, call the appropriate Verification System function/endpoint. See [`Verification System Deep Dive`](../../architecture/verification_system/verification_system_deep_dive.md).
6.  **Write Unit/Integration Tests:** Create tests in `backend/tests/` covering the service logic and the API endpoint interaction (using `TestClient`). Mock dependencies (like Verification System calls or database sessions) appropriately for unit tests.
7.  **Local Testing:** Run the backend server (`uvicorn ...`) and test the endpoint using `curl`, Postman, or ideally, by integrating it with the frontend (see Workflow C).

### Workflow B: Creating a New React UI Component

1.  **Define Component:** Determine the component's purpose, props (API), state, and visual appearance. Create a spec document if it's a complex/reusable component, potentially in `docs/components/ui_components/`. See [`Building UI Component Guide`](./building_ui_component.md).
2.  **Create Files:** Create the component file (e.g., `frontend/src/components/NewFeature/NewFeature.tsx`) and associated style file (e.g., `NewFeature.module.css`).
3.  **Implement Component Logic:** Write the React/TypeScript code. Use hooks (`useState`, `useEffect`, etc.) for state and side effects. Follow React best practices.
4.  **Styling:** Apply styles using CSS Modules or the project's chosen styling solution, adhering to the general style guide.
5.  **Integrate Validation Components (Crucial):** If the component handles user input subject to ethical rules, displays sensitive data, or interacts with specific APIs, integrate the relevant UI Validation components (`CoreValuesValidator`, `APIValidator`, `DataTraceability`) as per [`UI Validation Examples`](./ui_validation_examples.md).
6.  **Write Unit/Component Tests:** Create tests in `frontend/src/components/NewFeature/NewFeature.test.tsx` using Jest and React Testing Library. Test component rendering, state changes, prop handling, and interactions. Mock API calls or context providers as needed.
7.  **Local Testing:** Run the frontend dev server (`npm start`) and view/interact with the component in isolation (using Storybook, if set up) or integrated into a page. Check console for errors, including those from validation components.

### Workflow C: Connecting Frontend Component to Backend API

1.  **Identify/Create API Service:** In `frontend/src/services/`, locate or create the function responsible for calling the relevant backend endpoint (e.g., `apiClient.ts`, `userService.ts`). Use `Workspace` or `axios`.
2.  **Call Service from Component:** Use `useEffect` or event handlers (e.g., `onSubmit`) in your component (from Workflow B) to call the API service function. Handle loading states, responses, and errors.
3.  **Integrate `APIValidator` (Dev Mode):** Wrap the API call with `APIValidator` checks (as shown in [`UI Validation Examples`](./ui_validation_examples.md)) to validate request/response schemas during development.
4.  **Update State:** Update the component's state based on the API response.
5.  **Testing:** Update component tests to mock the API service calls and verify the component behaves correctly in different API response scenarios (loading, success, error). Consider integration tests if applicable.

### Workflow D: Fixing a Bug

1.  **Reproduce the Bug:** Use the steps in the bug report issue to reliably reproduce the bug locally.
2.  **Identify the Cause:** Use browser dev tools, backend logs, debuggers, and your understanding of the relevant code (frontend or backend) to pinpoint the source of the bug.
3.  **Write a Failing Test:** Before fixing, write a unit or integration test that specifically fails because of the bug. This confirms you've identified the issue and prevents regressions.
4.  **Fix the Bug:** Correct the code.
5.  **Run Tests:** Ensure the previously failing test now passes, and *all other* tests still pass.
6.  **Verify Fix:** Manually verify the fix locally by repeating the reproduction steps.
7.  **Commit:** Use a `fix:` prefix in your Conventional Commit message (e.g., `fix: prevent duplicate profile submissions`).

This guide provides a framework. Always refer to the specific linked documents for detailed standards and implementation patterns. Communicate early and often if you encounter roadblocks!

---
**Document Details**
- Title: Developer Workflow Guide
- Type: Developer Guide
- Version: 1.0.0
- Last Updated: 2025-04-05
---
End of Developer Workflow Guide
---


