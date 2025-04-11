# Contributing to ThinkAlike - Detailed Guide

Thank you for your interest in contributing to ThinkAlike! We welcome contributions from everyone, and we believe that a diverse and inclusive community is essential for building a truly ethical and innovative platform. Every contribution, no matter how small, is valuable and contributes to our mission of building a more humane and transparent digital world.

## Quick Overview

This page provides a comprehensive guide to contributing. For a more concise overview, you can also refer to:

**➡️ [View Contributing Overview](/docs/contributing_overview.md)**

**➡️ [View Quick Contributing Guide](/docs/contributing_quick.md)**

### Ways You Can Help - Quick Summary

* **Code:** Frontend (React/TS), Backend (Python/FastAPI), AI/ML.

* **Design:** UI/UX, Accessibility.

* **Documentation:** Writing guides, improving clarity, fixing errors.

* **Testing:** Writing automated tests, manual testing, ethical validation.

* **Community:** Helping others, moderation, outreach.

This guide provides detailed information on how to contribute to the project. Please read it carefully before submitting your first contribution.

**Crucially, ensure you understand the project's foundations by reviewing the [`SOURCE OF TRUTH - THINKALIKE PROJECT - MASTER REFERENCE.md`](docs/core/master_reference/master_reference.md) document first. This is essential reading and serves as the definitive guide for all aspects of the ThinkAlike project, including its overarching vision, ethical principles, and architectural guidelines. Also review the [`Onboarding Guide`](docs/core/onboarding_guide.md) for project context.**

Adherence to our [`Code of Conduct`](docs/core/code_of_conduct.md) is expected in all project interactions.

## Ways to Contribute

There are many ways to contribute to ThinkAlike, regardless of your skill level or background. We encourage contributions that align with our core values of **transparency, user empowerment, and ethical implementation.**

### Code

Contribute to the frontend (React/TS planned), backend (Python/FastAPI), or AI models. We strive for "Perfect Coding" – code that is not only functional but also ethically sound, transparent, and well-tested. This includes:

* Implementing new features enhancing user empowerment, data traceability, and ethical connection.

* Fixing bugs and ensuring platform robustness and reliability.

* Refactoring and optimizing existing code for performance, maintainability, and ethical clarity.

* Writing comprehensive unit, integration, and UI tests, emphasizing UI-driven data validation and workflow testing. ([`Testing Plan`](docs/guides/developer_guides/testing_and_validation_plan.md))

### UI/UX Design

Help design and improve the user interface and user experience, focusing on **UI as a Validation Framework**, **Data Transparency**, and **Accessibility**:

* Creating UI mockups and prototypes embodying ethical design principles and user empowerment.

* Designing reusable UI components facilitating data visualization, user control, and workflow transparency.

* Conducting user research and gathering feedback to validate UI/UX choices and ensure user-centricity.

* Improving platform accessibility, ensuring inclusivity and usability for all users. ([`Accessibility Guide`](docs/guides/developer_guides/Accessibility_Guide.md))

### Documentation

Improve project documentation, write guides, and create onboarding materials, ensuring **clarity, accuracy, and accessibility** for all:

* Writing clear, concise, comprehensive documentation for code, APIs, UI components, adhering to "Source of Truth" guidelines.

* Creating tutorials and examples showcasing ethical implementation patterns and data traceability workflows.

* Improving onboarding and quickstart guides. Help keep our documentation portal ([https://thinkalike-project.onrender.com/](https://thinkalike-project.onrender.com/)) up-to-date.

* Translating documentation to broaden accessibility.

### Testing

Help ensure platform quality, security, and ethical integrity through rigorous testing:

* Writing unit, integration, and UI tests, focusing on **UI-driven data validation** and **workflow testing**. ([`Testing Plan`](docs/guides/developer_guides/testing_and_validation_plan.md))

* Performing manual testing, reporting bugs with detailed data traceability information.

* Participating in user acceptance testing (UAT), providing user-centric and ethical feedback.

* Developing new testing methodologies enhancing data validation, ethical compliance, and UI workflow integrity.

### AI Model Development

Contribute to AI model development, training, and ethical validation, ensuring **transparency, accountability, and user empowerment**:

* Developing new AI models aligned with Enlightenment 2.0 principles.

* Improving existing models (performance, ethical behavior, data traceability).

* Creating quality datasets, ensuring ethical sourcing and bias mitigation.

* Implementing ethical AI guidelines and bias mitigation techniques at code/algorithmic level with clear UI validation parameters. ([`AI Dev Guide`](docs/guides/developer_guides/ai/ai_model_development_guide.md))

### Ethical and Security Expertise

Help ensure adherence to ethical principles and security best practices ("Security by Transparency"):

* Participating in ethical reviews (platform, AI, data handling).

* Identifying and mitigating security vulnerabilities (data privacy, access control). ([`Security Plan`](docs/architecture/security/security_and_privacy_plan.md))

* Contributing to transparent ethical guidelines, security policies, and data governance frameworks.

### Community Engagement

Help grow and support the ThinkAlike community:

* Answering questions on GitHub, Discord, etc.

* Moderating discussions respectfully.

* Organizing events (online/real-world).

* Spreading the word (blog posts, social media).

## Our Development Methodology: Human & AI Swarming

ThinkAlike embraces **Swarming** (similar to Mob Programming) as a primary method for collaborative code development, documentation writing, and complex problem-solving. We believe this approach aligns strongly with our core values of collaboration, knowledge sharing, transparency, and collective ownership.

**What is Swarming?**

In our context, Swarming means a group of contributors (developers, designers, testers, documenters) working **together, on the same task, at the same time, typically sharing one screen** within a virtual environment. We rotate roles frequently to ensure active participation and learning.

Furthermore, our development process itself leverages a form of **Human-Artificial Swarm Intelligence**. We utilize AI assistants (like VS Code Copilot, specialized internal agents TBD) as active collaborators *within* our human swarms and individual workflows. AI assists with code generation, documentation drafting, testing, and analysis, augmenting our collective capabilities. However, **human oversight, critical judgment, and ethical validation remain paramount** for all AI contributions, adhering to the guidelines in our [AI Driven Workflow guide](docs/guides/developer_guides/ai/ai_driven_workflow.md). Our goal is a synergistic partnership where both human and artificial intelligence contribute to building ThinkAlike ethically and effectively.

**Why Swarming?**

* **High-Bandwidth Communication:** Real-time discussion and problem-solving.

* **Knowledge Sharing:** Team members learn from each other constantly.

* **Higher Code Quality:** Multiple eyes on the code lead to fewer bugs and better design.

* **Reduced Blockers:** The group can overcome obstacles more quickly.

* **Alignment with Values:** Embodies collaboration and collective effort.

**Roles within a Swarm:**

Roles typically rotate every short interval (e.g., 10-20 minutes):

* **Driver:** Controls the keyboard/editor, translating the Navigator's instructions into code/text. Focuses on the immediate task.

* **Navigator:** Guides the Driver on *what* to do next at a tactical level (e.g., "Let's create a function called...", "Add a test case for..."). Thinks slightly ahead.

* **Mob/Swarm Members:** Observe, research, anticipate problems, suggest alternatives, review code as it's written, answer questions, look up documentation. Thinks strategically.

**Tools We Use:**

* **Video Conferencing:** [e.g., Discord Stage/VC, Google Meet, Zoom - Specify Tool] with reliable screen sharing.

* **Remote Control/Pairing (Optional):** Tools like VS Code Live Share, Tuple, Pop might be used for shared control.

* **Shared Timer:** For role rotations (e.g., mobti.me, built-in timer).

* **Virtual Whiteboard (Optional):** For design/architecture discussions (e.g., Miro, Excalidraw).

* **Git Collaboration:** Often using tools like `git mob` ([https://github.com/rkotze/git-mob](https://github.com/rkotze/git-mob)) or agreed-upon commit message conventions to co-author commits.

**How to Participate in Swarming Sessions:**

1. **Find Sessions:** Check the [**Swarming Schedule / Calendar Link - TODO**] or the dedicated `#swarm-sessions` channel on our [Communication Platform - Link TODO]. Sessions might focus on specific features, bugs, or documentation tasks from the [GitHub Issues - Link TODO].
2. **Prerequisites:** Ensure you have the local development environment set up ([Installation Guide](docs/core/installation.md)). Familiarity with the issue being tackled is helpful but not always required – learning is part of the process!
3. **Join the Call:** Join the scheduled video call link.
4. **Introduce Yourself:** Briefly say hello when you join.
5. **Observe & Engage:** Initially, feel free to observe. Ask clarifying questions in the chat or briefly unmute. Offer suggestions or research findings when appropriate. Be ready to take on the Driver or Navigator role when it's your turn (or feel free to pass initially if you're just learning).

**Output & Workflow Integration:**

* **Code Commits:** Code produced during a swarm is typically committed at the end of the session or logical checkpoints. We use [Specify Commit Method - e.g., `git mob` co-authoring, or designated committer with co-authors listed in message].

* **Pull Requests:** The output of a swarm focused on a specific issue usually results in a Pull Request, following the standard PR process outlined below, but attributed to the swarm participants. Review might be expedited given the collaborative nature of its creation, but still requires checks.

* **Individual Work:** While swarming is preferred for complex tasks and feature development, individual work on smaller bugs, documentation fixes, or pre-swarm research is still welcome and necessary. Follow the standard Fork & PR workflow described below for individual contributions.

## Getting Started

Before you start contributing:

1. **Read the [SOURCE OF TRUTH - THINKALIKE PROJECT - MASTER REFERENCE.md](docs/core/master_reference/master_reference.md).** (ESSENTIAL READING - Start here!)
2. **Read the [Onboarding Guide](docs/core/onboarding_guide.md).** Also potentially useful: [Quickstart Guide](docs/guides/mvp_implementation_guide.pdf).
3. **Explore the [GitHub Repository](https://github.com/EosLumina/--ThinkAlike--).** Familiarize yourself with the project structure and codebase.
4. **Setup Locally:** Follow the [`Installation Guide`](docs/core/installation.md). Use the [`Troubleshooting Guide`](docs/architecture/deployment_troubleshooting.md) if needed.
5. **Join our Community:** Introduce yourself on our [Discord Server](https://discord.gg/TnAcWezH). Let us know your interests!
6. **Find an Issue:** Check the [Issues Tab](https://github.com/EosLumina/--ThinkAlike--/issues).

## Finding Something to Work On

1. **Issue Tracker:** Explore the [GitHub Issues](https://github.com/EosLumina/--ThinkAlike--/issues) page.
2. **Labels:** Filter by labels defined in the [`Issue Labels Guide`](docs/guides/developer_guides/issue_labels_guide.md), such as:

    * `good first issue`: Great for newcomers.

    * `help wanted`: Areas needing community support.

    * `area: frontend`, `area: backend`, `area: documentation`, `area: testing`, `area: ai / ml`, etc.

3. **Propose:** Have your own idea? Open an issue first to discuss it with the maintainers and community.
4. **Claim:** Comment on an unassigned issue you want to work on to let others know you're tackling it.

## Contribution Workflow

ThinkAlike follows a standard GitHub Fork & Pull Request workflow, emphasizing transparency and code quality:

1. **Assign/Claim Issue:** Make sure the issue you're working on is assigned to you or you've claimed it via comment.
2. **Fork the Repository:** Create your own fork of the main ThinkAlike repository ([https://github.com/EosLumina/--ThinkAlike--](https://github.com/EosLumina/--ThinkAlike--)) on GitHub.
3. **Clone Your Fork:** Clone your forked repository to your local machine:

```bash
git clone https://github.com/YOUR_USERNAME/--ThinkAlike--.git # Replace YOUR_USERNAME

cd --ThinkAlike--

```

4. **Create a Feature Branch:** For *each* contribution, create a *new* branch from the `main` branch. Use a descriptive name following the convention: `type/issue-number-short-description` (e.g., `feat/123-profile-video`). Refer to [`Issue Labels Guide`](docs/guides/developer_guides/issue_labels_guide.md) for types (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ui`, `ci`, `build`).
5. **Develop & Commit:** Implement your contribution:

    * Adhere to the [`Code Style Guide`](docs/guides/developer_guides/code_style_guide.md) and best practices. Write code that is transparent, well-documented, and ethically sound.

    * **Test Thoroughly:** *Before* committing, test rigorously, focusing on **UI-driven data validation** and workflow integrity. Add relevant tests (Unit, Integration, UI) following the [`Testing Plan`](docs/guides/developer_guides/testing_and_validation_plan.md). Use "UI as Validation" principles ([`UI Validation Examples`](docs/guides/developer_guides/ui_validation_examples.md)). Perform manual testing, checking data traceability and UI feedback loops.

    * **Document Code:** Use the [`Code Documentation Template`](docs/templates/code_documentation_template.md) for significant changes.

    * **Commit:** Use clear, descriptive commit messages following the [Conventional Commits](#commit-message-guidelines) format.

6. **Keep Updated:** Regularly rebase or merge the `main` branch from the upstream (original) repository into your feature branch to incorporate the latest changes (`git fetch upstream`, `git rebase upstream/main`).
7. **Push to Your Fork:** Push your branch to your forked repository on GitHub:

```bash
git push origin your-branch-name

```

8. **Create a Pull Request (PR):** Open a pull request from your branch on your fork to the `main` branch of the main ThinkAlike repository.

    * Use the PR template if available.

    * Provide a clear description of your changes. Link the relevant issue (e.g., `Closes #123`). Include screenshots/GIFs for UI changes.

    * Ensure all automated checks (CI) pass.

9. **Code Review and Collaboration:** Engage constructively with feedback from project maintainers and community members. Reviewers will check for functionality, code quality, testing, documentation, **ethical alignment**, security, data traceability, and UI/UX integration.
10. **Merge:** Once your PR is approved and passes all tests, a project maintainer will merge it into the `main` branch.

**Important Documentation Note:** If your PR adds, removes, renames, or moves any documentation files within the `docs/` directory, **please update the `files` array in `docs/index.html`** within the same Pull Request. This ensures the documentation portal navigation remains accurate.

## Code Style Guidelines

We are committed to "Perfect Coding" – technically excellent, ethically sound, transparent code. Please adhere to the detailed guidelines in the [`docs/guides/developer_guides/code_style_guide.md`](docs/guides/developer_guides/code_style_guide.md) file.

**Key aspects:**

* **Readability & Clarity:** Accessible, maintainable, auditable code.

* **Transparency & Data Traceability:** Code patterns enhancing data flow understanding.

* **Ethical Considerations in Code:** Implement ethical principles directly.

* **UI Validation Integration:** Design code for seamless UI validation.

* **Language Conventions:** Follow standards (PEP 8 for Python, Airbnb React Style Guide for JS, etc.).

## Documentation Guidelines

Comprehensive, accessible documentation is crucial. Follow these guidelines:

* **"Source of Truth" Alignment:** Consistent with [`MASTER_REFERENCE.md`](docs/core/master_reference/master_reference.md).

* **Format:** Use Markdown.

* **Principles:** Adhere to Clarity, Conciseness, Accuracy, Completeness, Structure (as per Source of Truth).

* **Examples/UI Integration:** Include code examples, UI screenshots, diagrams. Emphasize UI's role in validation.

* **API/Component Docs:** Provide comprehensive API docs (OpenAPI/Swagger) and UI component specs.

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

**Structure:**

    <type>[optional scope]: <description>

    [optional body]

    [optional footer(s)]

* **`<type>`:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ui`, `ci`, `build`.

* **`[optional scope]`:** Area of change (e.g., `ui`, `api`, `database`, `auth`, `matching-algorithm`, `docs-onboarding`).

* **`<description>`:** Short, imperative mood, present tense, lowercase, no period (e.g., `implement ethical weighting`).

* **`[optional body]`:** Longer explanation, context, details. Use bullets if needed.

* **`[optional footer(s)]`:** Reference issues (`Fixes #123`), Breaking Changes (`BREAKING CHANGE:`).

**Examples:**

    feat(matching-algorithm): implement ethically weighted matching algorithm

    This implements the core value-based matching, incorporating ethical weighting and user controls per specs.

    * Prioritizes Value Nodes.

    * Allows user customization of value importance.

    * Integrates with DataTraceability for visualization.

    docs: update CONTRIBUTING.md with detailed guidelines

    fix(ui): resolve mobile layout issue in ProfileScreen

    Adjusted CSS for responsive layout. Tested on simulators.
    Fixes #456

## Code Review Process

All contributions undergo code review by maintainers and community members.

**Review Focus:**

* **Functionality:** Correct and efficient implementation.

* **Code Quality:** Clean, readable, documented, maintainable, follows style guide.

* **Ethical Compliance:** Adheres to [`Ethical Guidelines`](docs/core/ethics/ethical_guidelines.md), promotes transparency, user empowerment.

* **Testing:** Adequate tests (Unit, Integration, UI) validating code, robustness, ethical integrity via UI validation.

* **Data Traceability:** Clear data flows, effective use of UI for visualization/validation.

* **Security:** Secure coding practices, data privacy.

* **UI/UX:** Seamless integration, enhances user experience, promotes transparency/control.

Engage constructively with feedback. Code review is collaborative.

## Community and Communication

* **GitHub Repository:** [https://github.com/EosLumina/--ThinkAlike--](https://github.com/EosLumina/--ThinkAlike--) (Code, Issues, Technical Discussions)

* **Discord Server:** [https://discord.gg/TnAcWezH](https://discord.gg/TnAcWezH) (Real-time communication, Community Discussions, Q&A, Updates)

We encourage open communication, respectful dialogue, and collaborative problem-solving.

## Using AI Coding Assistants

We encourage using AI assistants (Copilot, Gemini) to improve efficiency, but **you are responsible for your contributions.** Treat AI as an *augmenting tool*, not a replacement for understanding, critical thinking, and ethical judgment.

**Best Practices:**

* **Understand Suggestions:** **Carefully review, understand, and validate** all AI-generated code.

* **Test Rigorously:** Test AI code thoroughly, especially edge cases, security, ethics. Use UI validation components.

* **Ethical Alignment:** Ensure AI code aligns with ThinkAlike's principles (no bias, opacity, manipulation). Use Verification System/UI validation.

* **Use for Repetitive Tasks:** Leverage AI for boilerplate/repetitive tasks, retaining human oversight on critical decisions.

* **Provide Clear Prompts:** Give specific context, specifications (link docs), and **ethical requirements**.

**Example Prompts (Tailored for ThinkAlike):**

* **Understanding a Component:**

        Explain the purpose and functionality of the following ThinkAlike React component,
        how it supports data traceability/user empowerment, prop meanings,
        and expected data types:
        [Paste component code]

* **Writing Tests (UI Validation Focus):**

        Write a pytest unit test for this Python function, focusing on data validation
        and using UI data feedback loops to verify output correctness and
        ethical data handling:
        [Paste function code]

* **Refactoring (Ethical Clarity):**

        Refactor this ThinkAlike JS code for readability, transparency, ethical clarity.
        Explain changes and how they enhance data traceability/user understanding:
        [Paste code]

* **Documentation (Transparency Focus):**

        Write a JSDoc comment for this ThinkAlike React component, explaining how it
        promotes data transparency and user control:
        [Paste component code]

* **Debugging (Ethical Lens):**

        Explain error: [Error message].
        Analyze the code for potential ethical issues (data handling/bias).
        Code:
        [Paste code]

* **Writing Commit Messages:**

        Write a conventional commit message for this change per ThinkAlike guidelines,
        emphasizing improvements to data traceability or ethical alignment:
        [Describe change briefly]

---

Thank you for contributing to building a more ethical and human-centered digital world with ThinkAlike!

---

**Document Details**

* Title: Contributing to ThinkAlike - Detailed Guide

* Type: Core Documentation

* Version: 1.0.0

* Last Updated: 2025-04-05

---

End of Contributing to ThinkAlike - Detailed Guide

---
