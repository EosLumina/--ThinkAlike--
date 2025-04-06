# Project Overview

## Introduction

ThinkAlike is an **open-source platform** designed to foster **genuine human connections** through **ethical technology** and **user empowerment**. It moves beyond superficial online interactions, aiming to help users:

* **Discover Themselves:** Explore values, beliefs, perspectives, and aspirations, primarily via **Mode 1 (Narrative Onboarding)**.
* **Connect with Like-Minded Individuals:** Find value-aligned connections using transparent **Mode 2 (Profile Discovery)** features.
* **Build Meaningful Relationships:** Bridge online interactions to real-world community and collaboration via **Mode 3 (Community Building)**.
* **Collaborate:** Build real-world connections within communities.
* **Contribute to a Better Future:** Participate in a community dedicated to building responsible, human-centered technology.

ThinkAlike leverages AI as a *tool* to *enhance* human connection and insight, not replace user agency. The platform prioritizes **Radical Transparency**, **User Sovereignty**, and ethical data handling, built on the principles of **"Enlightenment 2.0"** – using technology to promote reason, knowledge, and human flourishing ([See Principles](./enlightenment_2_0/ENLIGHTENMENT_2_0_PRINCIPLES.md)). It stands as a conscious alternative to exploitative digital platforms.

**(Refer to the [`MASTER_REFERENCE.md`](./master_reference.md) for definitive concepts and terminology).**

## Core Values

ThinkAlike is guided by the following core values:

* **Human-Centered Approach:** Prioritizing user well-being, dignity, and agency.
* **Ethical AI:** Ensuring AI is transparent, explainable, fair, and user-controlled. ([AI Dev Guide](../guides/developer_guides/ai/ai_model_development_guide.md))
* **Transparency & Traceability:** Open data workflows ([DataTraceability Spec](../components/ui_components/data_traceability.md)), auditable systems ([Verification System Spec](../architecture/verification_system/verification_system.md)), and auditable code.
* **User Empowerment & Sovereignty:** Giving users full control over their data and experience ([Data Handling Policy](../guides/developer_guides/data_handling_policy_guide.md), [Security Plan](../architecture/security/security_and_privacy_plan.md)).
* **Authenticity:** Fostering genuine, value-based connections.
* **Community & Positive Anarchism:** Enabling decentralized, self-governing communities and collaboration through voluntary association and mutual aid. ([Community Mode Spec](../architecture/modes/community_mode/community_mode_spec.md), [Ethos](./ethics/ethos.md)).
* **Inclusivity & Accessibility:** Designing for everyone ([Accessibility Guide](../guides/developer_guides/Accessibility_Guide.md)).
* **Privacy & Security:** Protecting user data ([Security Plan](../architecture/security/security_and_privacy_plan.md)).
* **Bias Mitigation:** Actively addressing potential biases in AI models.

**(See full details in [`Ethical Guidelines`](./ethics/ethical_guidelines.md)).**

## Key Features & Concepts

ThinkAlike's functionality is organized around several key areas and concepts:

* **Three Interaction Modes:**
    1.  **Mode 1: Personalized Narrative Journeys:** An interactive experience helping users explore values via guided prompts, assisted by an AI agent. ([Modes Overview](../architecture/modes/modes_overview.md))
    2.  **Mode 2: Profile Discovery & Connection:** Users explore potential connections based on Value Profiles, interacting via AI Clones/Avatars and initiating connections through Narrative Compatibility Tests.
    3.  **Mode 3: Community Building Tools:** Features facilitating decentralized community formation, governance, communication, and collaboration.
* **Value Profiles:** Nuanced, dynamic user representations of values, stances, and interests, driving connections.
* **Ethical AI Matching:** An intelligent system connecting users based on shared values and lifestyles, *not* superficial metrics. The AI's reasoning is transparent and explainable. ([Matching Algorithm Guide](../guides/developer_guides/matching_algorithm_guide.md)).
* **Data Traceability Visualization:** A unique, interactive UI component visually demonstrating data origins, usage, and influence on AI recommendations, central to our transparency commitment. ([DataTraceability Spec](../components/ui_components/data_traceability.md))
* **AI Clones / AI-Powered Video Avatars:** Dynamic visual/interactive representations of users, enhancing understanding in Mode 1 & 2 before direct connection.
* **Narrative Compatibility Tests:** User-initiated interaction gates in Mode 2 to ensure alignment before deeper connection.
* **Decentralized Communities:** User-created and governed groups in Mode 3.
* **UI as Validation Framework:** A unique approach using UI components for real-time testing, validation, and ethical enforcement during development. ([UI Validation Examples](../guides/developer_guides/ui_validation_examples.md)).
* **Verification System:** A backend engine ensuring system operations align with ethical and functional rules. ([Verification System Spec](../architecture/verification_system/verification_system.md))
* **Collective Empowerment:** Features supporting group collaboration, shared data understanding, and potentially collective data/privacy preference setting within communities.

## Technology Stack

* **Frontend:** React (Create React App, TypeScript planned), Zustand (State Management recommended)
* **Backend:** Python 3.9+, FastAPI, SQLAlchemy (ORM)
* **Database:** SQLite (Development), PostgreSQL (Production), Alembic (Migrations)
* **Authentication:** JWT
* **AI/ML:** Python libraries (Initially rule-based, planning for advanced models like collaborative filtering, NLP. See [AI Dev Guide](../guides/developer_guides/ai/ai_model_development_guide.md))
* **Deployment:** Render (initially), Docker
* **Documentation:** Markdown, Mermaid.js, Highlight.js (rendered via `docs/index.html`), with plans to explore static site generators like MkDocs.

## Architecture

ThinkAlike follows a modular, three-tier architecture focused on separation of concerns, testability, and ethical alignment:

1.  **Presentation Layer (UI):** React frontend.
2.  **Application Layer (API, Logic):** Python/FastAPI backend, business logic, AI integration.
3.  **Data Layer (Database, Storage):** SQLite/PostgreSQL persistence.

See the [`Architectural Overview`](../architecture/architectural_overview.md) and [`Architectural Design Specifications`](../architecture/design/architectural_design_specifications.md) for details. *(A Mermaid diagram illustrating the architecture is also included in the `ONBOARDING_GUIDE.md` file.)*

## Getting Involved

We welcome contributors!

* **Start Here:** Read the [`Onboarding Guide`](./onboarding_guide.md).
* **Contribution Process:** Follow the [`Contribution Guidelines`](./contributing.md).
* **Setup:** Use the [`Installation Guide`](./installation.md). If you get stuck, consult the [`Troubleshooting Guide`](../architecture/deployment_troubleshooting.md).
* **Explore & Connect:**
    * Join our Discord server: [https://discord.gg/TnAcWezH](https://discord.gg/TnAcWezH)
    * Explore the codebase on GitHub: [https://github.com/EosLumina/--ThinkAlike--](https://github.com/EosLumina/--ThinkAlike--)
    * Review the documentation via the Portal (see below).
    * Find tasks: Look for "good first issue" on GitHub: [https://github.com/EosLumina/--ThinkAlike--/issues](https://github.com/EosLumina/--ThinkAlike--/issues)

## Documentation Portal

Access all project documentation via the live portal: [https://thinkalike-project.onrender.com/](https://thinkalike-project.onrender.com/) (or current URL)

## License

* **Code:** Licensed under the [MIT License](LICENSE) (see the `LICENSE` file in the root directory).
* **Documentation & Visual Assets:** Licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). Please respect attribution, non-commercial use, and no derivatives. See [`README.md`](../readme.md) for more details.
