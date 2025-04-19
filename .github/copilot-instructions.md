- @azure Rule - Use Azure Best Practices: When generating code for Azure, running terminal commands for Azure, or performing operations related to Azure, invoke your `azure_development-get_best_practices` tool if available.

Here’s a prompt you can add to your repository (for Copilot or any AI assistant) to help analyze, repair, and progress your project holistically, with a focus on workflows and best practices:

---

**Prompt for Copilot or AI Assistant:**

---

You are assisting with the ThinkAlike project, a multi-component open-source platform with a Python backend, a React/TypeScript frontend, and extensive documentation. The project uses GitHub Actions for CI/CD, with workflows for linting, testing, security, and (optionally) Docker builds.

**Project Structure:**
- backend: Python FastAPI app, agents, algorithms, database, and tests.
- frontend: React app with TypeScript, modern tooling, and tests.
- docs: Documentation, including DevOps and workflow guides.
- workflows: Contains CI/CD workflows.

**Current Goals:**
- Ensure all workflows are valid, minimal, and reference only available secrets, files, and steps.
- Remove or comment out steps that require unavailable credentials (like DockerHub).
- Split workflows by concern (backend, frontend, docs) if appropriate, following ci_cd_workflow_reference.md.save.
- Fix build/test errors, especially TypeScript/React errors and Python test failures.
- Help stage and commit only necessary files for each logical change.
- Recommend next steps for project health and workflow improvement.
- Document all changes and rationale.

**Best Practices:**
- Use Azure best practices for any cloud-related code or workflow.
- Prioritize ethical, secure, and maintainable solutions.
- Reference and align with documentation in docs where possible.

**Instructions:**
1. Analyze the workspace for inconsistencies, misconfigurations, or missing files in workflows, backend, frontend, and docs.
2. Repair and optimize workflows, ensuring ci.yml (and any other active workflows) are valid and minimal.
3. Suggest or automate splitting workflows if appropriate.
4. Check for and fix build/test errors.
5. Guide on clean commits.
6. Recommend next steps.
7. Document changes and rationale.
