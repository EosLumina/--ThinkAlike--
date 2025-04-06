# GitHub Issue Labels Guide

---

## 1. Introduction

This guide defines the standard set of labels used in the ThinkAlike project's GitHub Issue tracker ([Link to Issues - TODO: Add Link]). Consistent labeling helps us organize tasks, indicate priority and status, identify areas needing help, and allows contributors to easily filter and find issues relevant to their skills and interests.

Please use these labels appropriately when creating or triaging issues. Maintainers will strive to keep issues labeled correctly.

---

## 2. Issue Type Labels (`type:` prefix)

These labels indicate the fundamental nature of the issue. An issue should generally have **one** `type:` label.

*   `type: bug` 🐛
    *   **Description:** An error, unexpected behavior, or incorrect functionality in the existing codebase or deployed application.
    *   **Examples:** API endpoint returning wrong status code, UI component rendering incorrectly, crash during specific workflow.

*   `type: feature` ✨
    *   **Description:** A request for a new feature, functionality, or enhancement to the platform.
    *   **Examples:** Add user profile picture upload, implement basic chat for connections, create a new visualization in DataTraceability.

*   `type: documentation` 📄
    *   **Description:** Issues related to creating, updating, correcting, or improving project documentation (`.md` files, code comments, API specs).
    *   **Examples:** Update installation guide for new dependency, clarify ethical guideline section, document a new API endpoint, add examples to UI component spec.

*   `type: chore` 🧹
    *   **Description:** Maintenance tasks, refactoring, dependency updates, build process improvements, CI/CD configuration, or other tasks not directly adding features or fixing user-facing bugs.
    *   **Examples:** Upgrade FastAPI version, refactor user service logic, configure automated dependency scanning, improve Dockerfile efficiency.

*   `type: testing` 🧪
    *   **Description:** Issues specifically related to adding, improving, or fixing automated or manual tests (unit, integration, E2E, performance, ethical, etc.).
    *   **Examples:** Add unit tests for matching algorithm module, implement E2E test for user registration flow, fix flaky UI component test.

*   `type: question` 🤔
    *   **Description:** Used for asking questions about the project, architecture, or implementation details, where a discussion is needed rather than a direct bug report or feature request. Can be closed once answered or converted to another type if action is needed.

---

## 3. Priority Labels (`priority:` prefix)

Indicate the urgency and importance of addressing the issue. An issue should generally have **one** `priority:` label (assigned primarily by maintainers).

*   `priority: critical` 🔥
    *   **Description:** Must be addressed immediately. Blocks releases or core functionality, security vulnerability, significant data corruption risk.

*   `priority: high` ⬆️
    *   **Description:** Important issue significantly impacting users or development, should be addressed soon (e.g., in the current or next sprint/milestone).

*   `priority: medium` ↔️
    *   **Description:** Standard priority for most bugs and features. Should be addressed in a reasonable timeframe.

*   `priority: low` ⬇️
    *   **Description:** Minor issue, nice-to-have feature, or task that can be deferred without significant impact.

---

## 4. Status Labels (`status:` prefix)

Track the current state of the issue in the workflow.

*   `status: 0 - backlog`
    *   **Description:** Acknowledged issue or feature request, not currently scheduled or being worked on. Needs triage/prioritization.

*   `status: 1 - todo / needs triage`
    *   **Description:** Ready to be picked up, needs assignment or further investigation/discussion to clarify requirements.

*   `status: 2 - in progress`
    *   **Description:** Actively being worked on by an assigned contributor.

*   `status: 3 - needs review`
    *   **Description:** A Pull Request (PR) has been submitted and is awaiting code review.

*   `status: 4 - blocked`
    *   **Description:** Progress is blocked by another issue, external dependency, or requires further information. Add a comment explaining the blocker.

*   `status: 5 - completed / closed`
    *   **Description:** Issue resolved, feature implemented, PR merged, or question answered. (Handled automatically when closing issues/PRs).

*   `status: wontfix / invalid`
    *   **Description:** Issue will not be addressed (e.g., out of scope, works as intended, cannot reproduce). Provide explanation when closing with this status.

---

## 5. Area / Module Labels (`area:` prefix)

Identify the part(s) of the project the issue relates to. An issue can have **multiple** `area:` labels.

*   `area: frontend / ui` 🖥️
*   `area: backend / api` ⚙️
*   `area: database` 💾
*   `area: ai / ml` 🤖
*   `area: mode-1` (Narrative)
*   `area: mode-2` (Discovery)
*   `area: mode-3` (Community)
*   `area: verification-system` 🛡️
*   `area: authentication` 🔑
*   `area: documentation` 📚
*   `area: testing` 🔬
*   `area: deployment / ci-cd` 🚀
*   `area: accessibility` ♿
*   `area: security` 🔒
*   `area: performance` ⚡

---

## 6. Labels for Contributors

These help new contributors find suitable tasks.

*   `good first issue` 👍
    *   **Description:** Issue deemed suitable for contributors new to the project. Should be well-defined with clear requirements and limited scope.

*   `help wanted` 🙏
    *   **Description:** Issue where the core team would particularly appreciate community contributions. May range in difficulty.

---

## 7. How to Use Labels

*   **Creators:** When opening an issue, try to apply the most relevant `type:` and `area:` labels. Add details in the description.
*   **Contributors:** Use labels to filter the issue tracker and find tasks matching your skills and interests. Look for `good first issue` or `help wanted`.
*   **Maintainers/Triagers:** Ensure issues are correctly labeled with `type:`, `priority:`, and `status:` labels. Assign `area:` labels accurately. Use labels to manage project boards and milestones.

Consistent labeling makes the issue tracker significantly more organized and useful for everyone involved in the ThinkAlike project.
