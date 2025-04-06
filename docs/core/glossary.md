# Project Glossary

## Introduction

This glossary defines key terms, acronyms, and concepts used throughout the ThinkAlike project documentation and platform. Understanding this terminology is crucial for effective collaboration and comprehension of the project's unique vision, architecture, and functionalities. Refer back to this glossary whenever encountering an unfamiliar term.

---

## Core Concepts & Philosophy

*   **Enlightenment 2.0:** The core philosophical framework underpinning ThinkAlike. It represents a contemporary adaptation of Enlightenment ideals (reason, humanism, progress) applied to the digital age, aiming to counteract techno-dystopian trends and leverage technology for human flourishing, ethical governance, and authentic connection. See [ENLIGHTENMENT_2_0_PRINCIPLES.md](enlightenment_2_0/ENLIGHTENMENT_2_0_PRINCIPLES.md).
*   **Positive Anarchism:** A constructive form of anarchism emphasizing decentralization, self-governance, mutual aid, horizontal collaboration, and the rejection of unjustified hierarchy. It's a key organizational principle for ThinkAlike, especially Mode 3. See [ENLIGHTENMENT_2_0_PRINCIPLES.md](enlightenment_2_0/ENLIGHTENMENT_2_0_PRINCIPLES.md).
*   **Ethical Humanism:** Placing human dignity, well-being, rights, and agency at the center of technological design and purpose. Technology serves humanity. See [ENLIGHTENMENT_2_0_PRINCIPLES.md](enlightenment_2_0/ENLIGHTENMENT_2_0_PRINCIPLES.md).
*   **Radical Transparency:** A commitment to openness, explainability, and auditability in algorithms, data handling, and platform governance. Opposes "black box" systems. See [ENLIGHTENMENT_2_0_PRINCIPLES.md](enlightenment_2_0/ENLIGHTENMENT_2_0_PRINCIPLES.md).
*   **User Empowerment / User Sovereignty:** Granting users maximum control over their data, digital experiences, privacy settings, and interactions with the platform and its AI. See [ENLIGHTENMENT_2_0_PRINCIPLES.md](enlightenment_2_0/ENLIGHTENMENT_2_0_PRINCIPLES.md).
*   **Authentic Connection:** Prioritizing genuine, meaningful relationships based on shared values and understanding, rather than superficial interactions. See [ENLIGHTENMENT_2_0_PRINCIPLES.md](enlightenment_2_0/ENLIGHTENMENT_2_0_PRINCIPLES.md).
*   **Redefined Progress:** Measuring success based on ethical and social advancement, human flourishing, and planetary well-being, not just technological or economic metrics. See [ENLIGHTENMENT_2_0_PRINCIPLES.md](enlightenment_2_0/ENLIGHTENMENT_2_0_PRINCIPLES.md).
*   **Eos Lumina:** The philosophical voice and guiding entity behind ThinkAlike's core vision and manifestos.
*   **Philosophical Manifesto of Eos Lumina:** The foundational text outlining the project's deep philosophical basis, critique of current systems, and vision for Enlightenment 2.0. See [manifesto.md](manifesto/manifesto.md).
*   **Ethical Guidelines:** The specific, actionable rules derived from core values that govern all development, design, and operation of ThinkAlike. See [ethical_guidelines.md](ethics/ethical_guidelines/ethical_guidelines.md).
*   **Perfect Coding:** The imperative within ThinkAlike that code must be not only technically excellent (clean, efficient, robust) but also ethically sound, transparent, well-documented, and aligned with core values.
*   **Source of Truth (MASTER_REFERENCE.md):** The central, authoritative document defining the project's vision, architecture, specifications, and principles. See [MASTER_REFERENCE.md](master_reference/master_reference.md).
*   **Zenith of Excellence:** The aesthetic and quality standard for ThinkAlike's design and documentation, emphasizing clarity, professionalism, modernity, and ethical integrity. See [Style Guide](../../guides/developer_guides/style_guide.md).

---

## Architecture & Technology

*   **Social LLM (Social Large Language Model):** A conceptual term describing ThinkAlike's overall function: processing the complex "language" of human values, interactions, and experiences to facilitate authentic connection and collective action, drawing inspiration from AI LLMs but focusing on social good.
*   **Node:** The fundamental unit representing a user within the ThinkAlike network. Each Node possesses a Value Profile.
*   **Value Profile:** A rich, dynamic dataset representing a user's core values, interests, narrative choices, preferences, and potentially activity data. It's the primary input for matching and personalization.
*   **AI Clone:** A dynamically generated visual avatar/representation of a User Node, created using AI analysis of the user's presentation video (voice, appearance, expressions) and styled to reflect their Value Profile. Used in Mode 1 reveal and Mode 2 browsing.
*   **Mode 1 (Narrative Mode):** The interactive, choose-your-own-adventure onboarding and primary AI-driven matching module ("Whispering Woods"). See [narrative_mode_spec.md](../../architecture/modes/narrative_mode/narrative_mode_spec.md).
*   **Mode 2 (Matching Mode):** The module focused on user-driven profile exploration (via AI Clones) and initiating connections gated by Narrative Compatibility Tests. See [matching_mode_spec.md](../../architecture/modes/matching_mode/matching_mode_spec.md).
*   **Mode 3 (Community Mode):** The module empowering users to create, manage, and participate in decentralized, self-governing, value-aligned communities. See [community_mode_spec.md](../../architecture/modes/community_mode/community_mode_spec.md).
*   **Verification System:** The cross-cutting architectural component ensuring ethical integrity, data traceability, and algorithmic accountability across all modes. See [verification_system.md](../../architecture/verification_system/verification_system.md).
*   **Ethical Knot:** A metaphorical term for the Verification System, highlighting its role in binding the core modules together through ethical enforcement.
*   **UI as Validation Framework:** The core principle that the User Interface components are designed not just for presentation and interaction, but also as active tools for testing and validating data flows, code implementation, ethical compliance, and AI behavior.
*   **Data Traceability:** The ability to track the origin, transformation, and usage of data throughout the platform. Made visible via components like `DataTraceability.jsx`.
*   **Ethical Weighting:** A mechanism within the Matching Algorithm that assigns greater importance to shared core ethical values when calculating compatibility scores. See [Developer Guide: Matching Algorithm](../../guides/developer_guides/matching_algorithm_guide.md).
*   **Matching Percentage:** A transparent score quantifying the value alignment between two User Nodes, generated by the Matching Algorithm.
*   **Narrative Compatibility Test:** A user-initiated, interactive narrative scenario in Mode 2 designed to assess compatibility between two users before enabling direct communication.
*   **Guiding Light:** An abstract visual representation (e.g., light wave) used in Narrative Mode before a match is fully revealed, or in Mode 2 to signify a "non-match" outcome after a Narrative Compatibility Test.
*   **Community Joining Gate:** Mechanisms (like Matching Percentage thresholds or Narrative Compatibility Tests) used by some Mode 3 communities to ensure value alignment among new members.
*   **API Validator:** A reusable UI component for displaying transparent feedback on API call status, requests, responses, and validation results. See [APIValidator.md](../components/ui_components/APIValidator.md).
*   **CoreValuesValidator:** A reusable UI component for visually validating and displaying alignment with ThinkAlike's core ethical principles in specific contexts. See [CoreValuesValidator.md](../components/ui_components/CoreValuesValidator.md).
*   **DataDisplay:** A foundational reusable UI component for consistently rendering individual data points with integrated validation and traceability cues. See [DataDisplay.md](../components/ui_components/DataDisplay.md).
*   **UserForm:** A standardized reusable UI component for handling user data input, incorporating validation and clear feedback. See [UserForm.md](../components/ui_components/UserForm.md).
*   **Security Status Indicator:** A persistent UI component providing real-time visual feedback on the user's data security status. See [Security_Status_Indicator.md](../components/ui_components/Security_Status_Indicator.md).
*   **Data Explorer Panel:** A UI panel allowing users to visualize, control, and understand their data within the platform. See [Data_Explorer_Panel.md](../../guides/ui_component_specs/data_explorer_panel.md).
*   **AI Transparency Log:** A UI component providing a user-readable log of AI decisions, data influences, and ethical parameters. See [ai_transparency_log.md](../../guides/developer_guides/ai/ai_transparency_log.md).
*   **FastAPI:** The Python web framework used for the backend API.
*   **React:** The JavaScript library used for the frontend UI.
*   **PostgreSQL:** The relational database system planned for production.
*   **SQLite:** The file-based database system used for local development.
*   **Render:** The cloud platform targeted for deployment. See [Deployment_Guide.md](../../guides/implementation_guides/Deployment_Guide.md).
*   **JWT (JSON Web Token):** A standard used for securely transmitting information between parties, often used for authentication.
*   **CORS (Cross-Origin Resource Sharing):** A browser security feature that restricts web pages from making requests to a different domain than the one that served the web page. Needs configuration on the backend.
*   **WCAG (Web Content Accessibility Guidelines):** International standards for web accessibility, ensuring content is usable by people with diverse abilities.
*   **XAI (Explainable AI):** Techniques and methods aimed at making AI decision-making processes understandable to humans.

---

## Project & Community

*   **MVP (Minimum Viable Product):** The initial version of ThinkAlike focused on core features demonstrating the primary vision (profile building, simple matching, traceability visualization, ethical foundation). See [mvp_implementation_guide.md](../../guides/implementation_guides/mvp_implementation_guide.md).
*   **UAT (User Acceptance Testing):** Testing conducted with real end-users to ensure the platform meets their needs and expectations.
*   **CI/CD (Continuous Integration / Continuous Deployment/Delivery):** Automated processes for building, testing, and deploying code changes.
*   **Conventional Commits:** A specification for standardized commit message formatting to create an explicit commit history. See [CONTRIBUTING.md](../../core/contributing.md).

*(This glossary will be updated as the project evolves and new terminology is introduced.)*

---
