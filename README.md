# ThinkAlike

**Connecting Like-Minded Individuals for Authentic Connection & Systemic Change**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/discord/YOUR_DISCORD_ID?label=Discord&logo=discord&color=7289DA)](https://discord.gg/TnAcWezH) <!-- TODO: Replace YOUR_DISCORD_ID -->
[![Docs CI Status](https://github.com/EosLumina/--ThinkAlike--/workflows/Docs%20CI%20Workflow/badge.svg)](https://github.com/EosLumina/--ThinkAlike--/actions?query=workflow%3A%22Docs+CI+Workflow%22) <!-- Verify Workflow Name -->
<!-- TODO: Add Build Status Badge -->
<!-- TODO: Add Coverage Badge -->

---

**ThinkAlike is a revolutionary open-source platform reimagining digital connection.** In a world often dominated by superficial interactions and opaque algorithms, ThinkAlike offers a different path. We are building a system designed to foster genuine human connection, helping users discover themselves, connect with like-minded individuals based on shared values, build meaningful relationships, and contribute to a better future.

We leverage AI to **enhance** human connection, *not* replace it. Our development is guided by principles of **transparency, user agency, ethical data handling,** and the concept of **"Enlightenment 2.0,"** actively challenging exploitative tech paradigms. ThinkAlike is more than an app; it's a movement towards a more human-centered digital world, built collaboratively and openly.

A unique aspect of this project is our **UI-Driven Validation approach**: the User Interface itself serves as a critical testing and validation tool, ensuring our technology remains trustworthy, user-centric, and aligned with our ethical commitments in real-time.

---

## What Makes ThinkAlike Different?

* **Enlightenment 2.0 Core:** Guided by reason, ethical humanism, radical transparency, user sovereignty, positive anarchism, and a redefined sense of progress focused on well-being and **liberated time (Otium)**. ([Read Principles](docs/core/enlightenment_2_0/enlightenment_2_0_principles.md))
* **Ethical AI & Value-Based Matching:** Intelligent connections based on deep value alignment. AI *assists* self-discovery and connection, transparently and ethically. ([Ethical Guidelines](docs/core/ethics/ethical_guidelines.md), [AI Dev Guide](docs/guides/developer_guides/ai/ai_model_development_guide.md))
* **Radical Transparency & Data Traceability:** Unique, interactive visualizations (`DataTraceability`) show users *exactly* how their data informs AI decisions. No black boxes. ([Component Spec](docs/components/ui_components/data_traceability.md), [AI Transparency Log](docs/guides/developer_guides/ai/ai_transparency_log.md))
* **User Empowerment & Sovereignty:** Complete user control over data, privacy, AI interactions, and community participation. Your data belongs to you. ([Core Concepts Explained](docs/vision/core_concepts.md))
* **UI as Validation Framework:** Our innovative approach uses the UI itself as an active tool for testing and validating code, data flow, performance, and ethical compliance in real-time. ([UI Validation Examples](docs/guides/developer_guides/ui_validation_examples.md))
* **Decentralized Community Building (Mode 3):** Tools for creating, discovering, and participating in user-governed communities based on shared values. ([Community Mode Spec](docs/architecture/modes/community_mode/community_mode_spec.md))
* **Open Source & Community-Driven:** Built collaboratively via **Swarming** and individual contributions, inviting global scrutiny. ([Contributing Guide](docs/core/contributing.md))

---

## Everyday Use Cases

* Find meaningful social connections based on shared values.
* Embark on interactive self-discovery journeys guided by ethical AI.
* Build and join purpose-driven communities for collaboration.
* Experience transparent data handling and maintain control.
* Utilize the platform for ethical AI development and research via UI-driven validation.

---

## Platform Structure: Key Modes

ThinkAlike guides users through distinct stages:

1. **Mode 1: Narrative Onboarding & Match Reveal:** AI-guided self-discovery and initial value-based match suggestions. ([Mode 1 Spec](docs/architecture/modes/narrative_onboarding_mode/mode1_narrative_onboarding_spec.md))
2. **Mode 2: Profile Discovery & Connection:** User-driven exploration of potential connections with transparent matching scores and compatibility tests. ([Mode 2 Spec](docs/architecture/modes/mode2_profile_discovery_spec.md))
3. **Mode 3: Community Building:** Tools for decentralized, value-aligned community creation and interaction. ([Community Mode Spec](docs/architecture/modes/community_mode/community_mode_spec.md))

---

## Technology Stack

* **Frontend:** React (TypeScript planned), Zustand (recommended), CSS Modules / Styled Components
* **Backend:** Python 3.9+, FastAPI, SQLAlchemy
* **Database:** SQLite (Development), PostgreSQL (Production)
* **API Communication:** RESTful APIs, JWT Auth
* **AI/ML:** Python libraries (Specifics evolving - see AI Dev Guide). Initial focus on rule-based systems, planning for more advanced models.
* **Deployment:** Render (initially), Docker
* **Documentation:** Markdown, Mermaid.js, Highlight.js (via `docs/index.html`)

---

## Quickstart for Contributors (TL;DR Setup)

Want to get coding quickly?

1. **Primary Setup:** Use the main **[Installation Guide](docs/core/installation.md)**.
2. **Alternative (MVP Focus):** The **[MVP Implementation Guide](docs/guides/implementation_guides/mvp_implementation_guide.md)** might be useful for focusing on core features.

*See the full Getting Started section below for essential context before contributing.*

---

## Getting Started (Comprehensive Guide)

### For All Users & Potential Contributors

* **Explore the Vision:** Understand the *why* behind ThinkAlike. Read the [Project Overview](docs/core/project_overview.md) and the [Manifesto](docs/core/manifesto/manifesto.md).
* **Browse Documentation:** Visit the live **Documentation Portal:** [https://thinkalike-project.onrender.com/](https://thinkalike-project.onrender.com/) (or current docs URL).
* **Join the Community:** Connect on **Discord:** [https://discord.gg/TnAcWezH](https://discord.gg/TnAcWezH).
* *(Live Application Link Coming Soon!)*

### For Contributors (Setting Up & Contributing)

Ready to contribute code, docs, or design?

1. **Onboarding (Highly Recommended):** Start with the **[Onboarding Guide](docs/core/onboarding_guide.md)** for a full project introduction, values, and architecture.
2. **Understand the Core:** Review the **[MASTER_REFERENCE.md](docs/core/master_reference.md)** (Source of Truth), **[Ethical Guidelines](docs/core/ethics/ethical_guidelines.md)**, and **[Ethos.md](docs/core/ethos.md)**. This context is crucial.
3. **Setup Locally:** Follow the **[Installation Guide](docs/core/installation.md)** or the alternative [MVP Implementation Guide](docs/guides/implementation_guides/mvp_implementation_guide.md).
4. **Troubleshooting:** Refer to the **[Troubleshooting Guide](docs/architecture/deployment_troubleshooting.md)** if you hit issues.
5. **How to Contribute:** ***Before coding***, read **[CONTRIBUTING.md](docs/core/contributing.md)** carefully for workflow, standards, and processes.
6. **Explore Key Code:** Check out the **DataTraceability component** at [ui/src/components/DataTraceability.jsx](ui/src/components/DataTraceability.jsx) *(Link may need updating)* and related docs linked below.

---

## Documentation

* **Live Portal:** [https://thinkalike-project.onrender.com/](https://thinkalike-project.onrender.com/) (or current live docs URL)
* **Source of Truth:** [docs/core/master_reference.md](docs/core/master_reference.md)
* **Dive Deeper:** Explore [Ethos](docs/ethos.md), [Core UI Components](docs/ui/core_ui_components.md), [Visual Style Guide](docs/guides/developer_guides/visual_style_guide.md), [DataTraceability Component Documentation](docs/ui/datatraceability_documentation.md).
* *Browse the full `docs/` directory for comprehensive info.*

---

## License

* **Code:** [MIT License](LICENSE).
* **Documentation & Visual Assets:** [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). Please respect attribution, non-commercial use, and no derivatives for `docs/` content, logos, and style guide assets to maintain project identity.

---

## Contact & Community

* **Discord:** [https://discord.gg/TnAcWezH](https://discord.gg/TnAcWezH) - ***Primary channel for interaction.***
* **GitHub Issues:** Bug reports & feature requests ([https://github.com/EosLumina/--ThinkAlike--/issues](https://github.com/EosLumina/--ThinkAlike--/issues))
* **GitHub Discussions:** Broader ideas & Q&A ([Link Here - TODO: Enable/Link Discussions if applicable])
* **Project Email:** [ThinkAlikeAI@proton.me](mailto:ThinkAlikeAI@proton.me) (General inquiries)
* **Lead Design Architect:** [Eos.Lumina@proton.me](mailto:Eos.Lumina@proton.me) (Design/UI/UX/Vision questions)

---

**The Future's Code is Unwritten. JOIN THE BUILD. IGNITE THE CHANGE.**
