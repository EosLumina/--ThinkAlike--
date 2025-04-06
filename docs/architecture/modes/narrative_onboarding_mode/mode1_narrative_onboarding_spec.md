// filepath: C:\--ThinkAlike--\docs\architecture\modes\narrative_onboarding_mode\mode1_narrative_onboarding_spec.md
# Narrative Mode Specification - Project

**Document Purpose:**

This document provides a **detailed specification for Narrative Mode** within the ThinkAlike project.  It outlines the functionality, features, user flows, data models, and technical considerations for implementing Narrative Mode, which serves as the onboarding, ideological injection, and documentation hub of the platform.

**I.  Core Functionality and Features:**

Narrative Mode serves several key purposes:

1. **User Onboarding and Platform Introduction:**
    * **Interactive Onboarding Narrative:**  Presents a compelling and engaging interactive narrative that guides new users through the core concepts of ThinkAlike, its mission, and its ethical principles (Enlightenment 2.0).
    * **Feature Discovery and Tutorials:**  Integrates interactive tutorials and feature highlights to introduce users to the functionalities of each Mode (Narrative, Matching, Community) and how to use them effectively.
    * **Value Proposition and Benefits:**  Clearly communicates the user value proposition of ThinkAlike, emphasizing its ethical upgrade, user empowerment, and potential for authentic connection.
    * **Call to Action to Participate:**  Concludes the onboarding narrative with a clear call to action, encouraging users to create their personal narratives and begin exploring the platform.

2. **"Philosophical Manifesto of Eos Lumina" Embodiment:**
    * **Interactive Manifesto Presentation:**  Presents the full "Philosophical Manifesto of Eos Lumina" in a dynamic and engaging digital format, moving beyond a static document.
    * **Thematic Exploration of Manifesto Principles:**  Allows users to explore the Manifesto's core principles (Positive Anarchism, Ethical Humanism, Radical Transparency, User Empowerment, Authentic Connection, Redefined Progress) in an interactive and thematic way.
    * **Multimedia Integration (Optional):**  Potentially incorporates multimedia elements (images, audio, video) to enhance the Manifesto's presentation and impact (future enhancement).
    * **User Annotation and Reflection (Optional):**  Potentially allows users to annotate, highlight, and save sections of the Manifesto for personal reflection and engagement (future enhancement).

3. **Personal Narrative Creation and Profile Building:**
    * **Guided Narrative Creation Flow:**  Provides a structured and guided flow for users to create their personal narratives, prompting them to articulate their values, interests, motivations, and vision.
    * **Value Elicitation Prompts:**  Includes prompts and questions specifically designed to elicit user values and ethical principles, ensuring these are central to their narratives.
    * **Rich Text Editor and Formatting Options:**  Offers a rich text editor with formatting options to allow users to create compelling and well-structured narratives.
    * **Privacy Settings for Narrative Visibility:**  Allows users to control the visibility of their narratives (e.g., public, only to matched users, private).
    * **Narrative Storage and Management:**  Provides secure and private storage for user narratives and allows users to easily edit and update them over time.

4. **AI Agent as Your Guide, Storyteller, and Mirror:**
    * **Narrative Facilitation:** Guides the user through the "Whispering Woods" adventure, presenting choices and adapting the story.
    * **Value Elicitation & Profile Building:** User choices implicitly and explicitly build their initial **Value Profile**.
    * **Contextual UI Guidance (Subtle & Optional):** Provides non-intrusive guidance on platform features *within the narrative flow*. Instead of explicit tutorials, it might offer reflections linking choices to platform concepts (e.g., "That choice reflects a strong leaning towards 'Community'. You can explore communities further in Mode 3 [subtle highlight]"). Guidance uses tooltips or optional "learn more" prompts.
    * **Ethos Alignment Assessment:** Internally calculates a dynamic **"E2.0 Alignment Score"** based on choices reflecting core ThinkAlike principles.
    * **Conditional Contributor Pledge:** If the Alignment Score reaches a threshold, presents the user with an *optional* **"Pledge to Architect"** agreement near the narrative's end.
    * **Initial Matching:** Uses the accumulated Value Profile data and Alignment Score to potentially reveal a "perfect match" (AI Clone) as the narrative conclusion.

5. **Documentation Hub and Project Knowledge Base:**
    * **Centralized Access to Project Documentation:**  Acts as a central hub for accessing all project documentation, including the "Source of Truth," Architectural Design Specs, Ethical Guidelines, API documentation, and user guides.
    * **Categorized and Searchable Documentation:**  Organizes documentation into logical categories and provides search functionality to allow users (and developers) to easily find specific information.
    * **Version Control and Update Tracking (Links to External System):**  Provides links to the version-controlled documentation repository (e.g., GitHub), allowing users to access the latest versions and track updates.
    * **Community Contribution to Documentation (Future Enhancement):**  Potentially allows for community contributions and feedback on documentation (future enhancement, e.g., through a linked wiki or collaborative documentation platform).

**II.  User Flows and Interactions:**

1. **New User Onboarding Flow:**
    * User lands on ThinkAlike platform (e.g., `index.html`).
    * Prominent entry point to "Narrative Mode / Onboarding Journey."
    * Interactive onboarding narrative begins, guiding user through:
        * Welcome and Introduction to ThinkAlike and Enlightenment 2.0.
        * Explanation of core principles (Positive Anarchism, Ethical Humanism, etc.).
        * Overview of the 3 Modes (Narrative, Matching, Community) and their functionalities.
        * Highlighting user value proposition and ethical commitments.
        * Tutorials and feature discovery elements interspersed throughout the narrative.
    * Call to action at the end of the narrative: "Create Your Narrative and Begin Your ThinkAlike Journey."
    * Transition to Personal Narrative Creation flow.

2. **Personal Narrative Creation Flow:**
    * User initiates "Create Narrative" from Onboarding flow or Profile settings.
    * Guided narrative creation interface is presented:
        * Welcome message and instructions.
        * Structured prompts and questions to guide narrative creation (value elicitation prompts, etc.).
        * Rich text editor with formatting options.
        * Progress indicator and save/draft functionality.
    * User inputs their narrative content.
    * User defines privacy settings for narrative visibility.
    * Narrative is saved to user profile and database.
    * User is presented with options to:
        * View their narrative.
        * Edit their narrative.
        * Proceed to Matching Mode or Community Mode.

3. **Documentation Hub Navigation:**
    * Users can access the Documentation Hub from the main navigation menu within Narrative Mode.
    * Documentation Hub presents a categorized and searchable index of all project documentation.
    * Users can browse categories or use search functionality to find specific documents.
    * Clicking on a documentation link opens the document content within the platform (or in a new tab/window, depending on implementation).

4. **AI Agent Interaction Flow:**
    * Narrative progresses, AI Agent provides subtle, contextual UI guidance prompts where relevant.
    * Backend calculates internal E2.0 Alignment Score based on choices.
    * (Conditional Step - Near End) If Alignment Score threshold met: AI Agent presents "Pledge to Architect" ([Contributor Agreement](../../legal/contributor_agreement.md)) as an optional narrative choice/screen.
    * User Accepts/Declines Pledge (Optional). If accepted, backend updates user role/flag (`POST /api/v1/contributor/agree` or integrated into `/narrative/choice`).
    * Narrative Climax: Based on final compatibility calculations:
        * If high match threshold met: "Perfect Match" reveal (AI Clone transition). Direct connection enabled. Optionally suggest contributor-specific next steps if pledge accepted (e.g., relevant community).
        * If lower match/no sufficient match: Narrative concludes with guidance towards Mode 2 discovery. Optionally suggest contributor next steps if pledge accepted.

**III. Data Model (Example - Conceptual):**
Use code with caution.
Markdown
NarrativeNode {
nodeId: UUID (Unique Identifier)
nodeType: Enum ['section', 'tutorial', 'prompt', 'manifesto_point', ...] // Type of narrative node
contentType: Enum ['text', 'image', 'video', 'audio', ...] // Type of content within the node
content: Text/Media // Actual narrative content
order: Integer // Order of node in the narrative flow
parentNodes: [NarrativeNodeId] // Links to parent nodes for branching narrative
childNodes: [NarrativeNodeId] // Links to child nodes for narrative progression
// ... other narrative node properties (styling, interactions, etc.)
}

UserNarrative {
userId: UUID (Foreign Key to User Profile)
narrativeContent: JSON/Structured Data // User-created narrative content, potentially linked to NarrativeNodes
privacySettings: Enum ['public', 'matched_users', 'private']
creationTimestamp: Timestamp
updateTimestamp: Timestamp
// ... other user narrative metadata
}

NarrativeSessionState {
userId: UUID
sessionId: UUID
currentNodeId: UUID
accumulatedValueMetrics: JSON
e2oAlignmentScore: Float // Internal alignment score
contributorPledgeStatus: Enum ['offered', 'accepted', 'declined']
// ... other session state properties
}

**IV. UI Components (Specific to Narrative Mode):**

* `NarrativeViewer`: Component for displaying and rendering interactive narrative content, handling navigation between narrative nodes, and managing user interactions.
* `NarrativeEditor`: Rich text editor component for users to create and edit their personal narratives, including formatting options and guided prompts.
* `DocumentationIndex`: Component for displaying a categorized and searchable index of project documentation.
* `ValueElicitationPrompt`: (Optional) Reusable component for presenting specific prompts designed to elicit user values within the narrative creation flow.

**V. API Endpoints (Backend - Examples):**

* `/api/narrative/onboarding`:  Returns data for the interactive onboarding narrative flow (structure and content of NarrativeNodes).
* `/api/narrative/manifesto`: Returns data for the interactive Manifesto presentation (structure and content of Manifesto NarrativeNodes).
* `/api/narrative/user-narrative`: (Authenticated)
  * `GET`: Returns the current user's narrative (if it exists).
  * `POST`: Creates a new user narrative.
  * `PUT`: Updates an existing user narrative.
  * `DELETE`: Deletes a user narrative.
* `/api/documentation/index`: Returns a structured index of all project documentation files.
* `/api/documentation/content/{documentName}`: Returns the content of a specific documentation file (e.g., Markdown content).
* `/api/v1/contributor/agree`: Updates user role/flag upon acceptance of the Contributor Pledge.

**VI.  Technical Considerations:**

* **Interactive Narrative Engine Implementation:**  Careful design and implementation of the interactive narrative engine is crucial for creating an engaging and user-friendly onboarding and Manifesto experience. Consider using a graph-based data structure or a state management library to manage the non-linear narrative flow.
* **Content Management System (CMS) for Documentation (Optional):**  For larger-scale documentation management and community contributions, consider integrating a lightweight CMS or static site generator to manage documentation files more efficiently (future enhancement).
* **Performance Optimization:**  Optimize performance for loading and rendering potentially large narrative content and documentation files, especially for users with slower internet connections.
* **Accessibility:**  Design Narrative Mode to be accessible to users with disabilities, adhering to accessibility guidelines (WCAG) for UI components and content presentation.
* **AI Agent Persona Consistency:** Requires careful design and prompt engineering to maintain a consistent, helpful, non-manipulative tone across its multiple roles (storyteller, guide, assessor, recruiter).
* **Contextual Guidance Implementation:** Needs backend logic to map narrative nodes to potential UI tutorial triggers and frontend ability to display these contextually (e.g., highlighting UI elements referenced by agent).
* **Alignment Scoring Logic:** Define and implement the algorithm for calculating the internal "E2.0 Alignment Score" based on narrative choices (requires careful ethical design and testing).

**VII.  Future Enhancements:**

* Multimedia integration within the Manifesto and onboarding narrative (images, audio, video).
* User annotation and highlighting features for the Manifesto.
* Community contribution mechanisms for documentation.
* More advanced narrative analytics to track user engagement and onboarding effectiveness.

---

---
**Document Details**
- Title: Narrative Mode Specification - Project
- Type: Architecture Documentation
- Version: 1.0.0
- Last Updated: 2025-04-05
---
End of Narrative Mode Specification - Project
---



