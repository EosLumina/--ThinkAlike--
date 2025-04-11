# Developer Guide: Value-Based Matching Algorithm

* --

## 1. Introduction

This guide provides a comprehensive overview for developers working on the ThinkAlike **Value-Based Matching
Algorithm**. This is a core backend component responsible for calculating compatibility (Matching Percentages) between
users, primarily informing **Mode 2 (Profile Discovery)** and the "perfect match" reveal in **Mode 1 (Narrative
Onboarding)**.

Its central purpose is to facilitate connections based on **deep value alignment and shared ethical principles**, moving
beyond superficial metrics. It implements **Ethical Weighting** and relies heavily on user **Value Profiles**, always
prioritizing **User Agency** and **Radical Transparency**.

This guide details the algorithm's architecture, data inputs, ethical weighting logic, integration with the Verification
System, and requirements for transparency via UI components like
[`DataTraceability`](../../components/ui_components/data_traceability.md). It adheres to principles in the
[MASTER_REFERENCE.md](../../core/master_reference.md) and [Ethical Guidelines](../../core/ethics/ethical_guidelines.md).

## 2. Purpose and Goals

*   **Identify Value-Aligned Connections:** Ethically calculate compatibility scores based on user **Value Profiles**.
*   **Prioritize Ethical Congruence:** Implement **Ethical Weighting** favoring connections aligned with [Enlightenment

1. 0 Principles](../../core/enlightenment_2_0/enlightenment_2_0_principles.md).

*   **Empower User Choice:** Provide transparent **Matching Percentages** and rationale (via `DataTraceability`) to

inform user decisions in Mode 2.

*   **Drive Mode 1 Reveal:** Provide the compatibility assessment needed for the potential "perfect match" reveal in

Mode 1.

*   **Foster Value-Driven Ecosystem:** Encourage connections grounded in shared ethical foundations.

## 3. Core Principles

*   **Value-Centricity:** **Value Profiles** are the primary input. Shared ethics > superficial similarity.
*   **Ethical Weighting:** Explicitly prioritize core ThinkAlike values in scoring.
*   **Transparency & Explainability (XAI):** Logic, weights, data flows documented ([Unified Data Model

Schema](../../architecture/database/unified_data_model_schema.md)) and designed for auditability ([Verification System
Spec](../../architecture/verification_system/verification_system.md)) and visualization ([`DataTraceability
Spec`](../../components/ui_components/data_traceability.md)).

*   **User Control:** Users manage their Value Profiles; algorithm respects consent for using external data ([Data

Integration Strategy](../../architecture/data_integration_strategy.md)).

*   **Data Privacy & Minimization:** Operates within [Data Handling Policy](./data_handling_policy_guide.md), uses

minimum necessary, consented data ethically.

*   **Fairness & Bias Mitigation:** Actively tested and refined to minimize demographic or value-based bias ([AI Ethical

Testing Guide](./ai/ai_ethical_testing_guide.md)).

## 4. Algorithm Architecture and Data Flow (Backend Service)

The Matching Algorithm logic typically resides within a dedicated backend service module (e.g.,
`backend/services/matching_service.py`) called by API endpoints like `POST /api/v1/match` (for generating
recommendations) or implicitly during Mode 1/Mode 2 operations.

### 4.1 Input Data: Value Profiles & Context

The algorithm consumes:

*   **Target User's Value Profile:** The profile of the user for whom matches are being calculated.
*   **Candidate Users' Value Profiles:** Profiles of other users to compare against.
*   **Value Profile Components:**
    *   Explicitly stated values/interests from user profile settings.
    *   Narrative-derived values/traits from Mode 1 choices.
    *   **(Optional/Consented):** Derived insights from connected external services (e.g., shared reading genres from

Goodreads). See [External API Integration Guide](./external_api_integration_guide.md).
    *   **(Future):** Potentially anonymized interaction data or community affiliations.
*   **Context (Optional):** Filters or specific parameters passed via the API request (e.g., `minMatchPercentage`,

specific values to filter by).

### 4.2 Calculation: Ethically Weighted Similarity Score

The core process compares User A's Value Profile to User B's:

1. **Feature Vector Creation:** Transform the diverse data points in each Value Profile into comparable feature vectors

or sets (e.g., sets of value tags, numerical vectors representing interest strengths).

1. **Component Similarity Calculation:** Calculate similarity scores for different *components* of the Value Profile:

    *   Explicit Value Similarity (e.g., Jaccard Index or weighted overlap on shared value tags).
    *   Narrative Archetype Similarity (if applicable, based on Mode 1 path analysis).
    *   Interest Similarity (e.g., cosine similarity on interest vectors, Jaccard on shared tags).
    *   External Data Similarity (e.g., shared books/artists/genres - only if consented).
1. **Ethical Weighting Application:** Apply the pre-defined `ETHICAL_WEIGHTS` to the similarity scores of *value-based

components*. Core ethical values contribute more significantly to the overall score.
    *   `WeightedValueScore = ValueSimilarity * EthicalWeight_ValueCategory`
1. **Aggregation & Normalization:** Combine the weighted value scores and other component similarity scores (potentially

with their own non-ethical weights reflecting importance) into a single **Matching Percentage** score, typically
normalized to a 0-100 or 0.0-1.0 scale. The exact aggregation formula needs careful design and documentation.

1. **Verification System Hook (Bias Check):** Optionally, before finalizing scores for a batch, send score distributions

and relevant demographic data (anonymized if possible) to the [Verification System
API](../../architecture/api/api_endpoints_verification_system.md) for fairness/bias checks. Results might flag potential
issues for review but should not automatically alter scores without transparent rules. See [VS Integration
Guide](./verification_system_integration_guide.md).

### 4.3 Output Data

The service utilizing the algorithm returns data suitable for the calling API endpoint:

*   List of matched `userId`s.
*   `matchingPercentage` score for each match.
*   `keySharedValues` / `contributingFactors`: Data points primarily responsible for the high score.
*   `traceability_data`: Structured graph data (`nodes`, `edges` with `ethicalWeight`) for rendering the match rationale

in the [`DataTraceability`](../../components/ui_components/data_traceability.md) component.

## 5. Ethical Weighting Implementation

*   **Taxonomy & Weights:** Defined centrally (e.g., config file, database table managed via Verification System

interface). Based on [Ethical Guidelines](../../core/ethics/ethical_guidelines.md). Rationale documented. Weights
subject to review/adjustment based on ethical testing and community feedback.
    ```python

    # Example Weights (Illustrative - Define centrally)
    ETHICAL_WEIGHTS = {
        "Transparency": 0.95, "UserEmpowerment": 0.95, "DataPrivacy": 0.9,
        "EthicalAI": 0.85, "CommunityCollaboration": 0.75, # ... etc.
    }
    NON_ETHICAL_WEIGHTS = { # Weights for non-core-value components
        "SharedInterests": 0.5, "ExternalDataOverlap": 0.3 # Lower weighting
    }
    ```

*   **Algorithm Integration:** Weights are applied during the Aggregation step (Step 4.2.4 above). Ensure the formula

correctly reflects the intended prioritization.

*   **Transparency:** The weighting concept explained in user guides. The *impact* visualized in `DataTraceability`

(e.g., thicker/brighter edges for ethically weighted shared values).

## 6. DataTraceability & Validation Integration

*   **Generating `traceability_data`:** The algorithm or calling service must construct the `graphData` object. Nodes

represent User A, User B, and key shared Values/Interests/Data Points. Edges connect users to these shared points. Edge
`styleProps` or implicit rendering rules in `DataTraceability` should reflect the `ethicalWeight` associated with the
shared value node.

*   **Explainability:** The generated graph *is* the primary explanation for the match score.
*   **Testing:** Unit tests must verify correct `traceability_data` generation for given inputs/scores. UI tests

validate `DataTraceability` renders the graph correctly based on this data.

## 7. Contribution Guidelines & Best Practices

*   **Code Quality:** Adhere to [Code Style Guide](./code_style_guide.md) (PEP 8, clarity, documentation).
*   **Testing:** **Crucial.** Write comprehensive `pytest` unit tests covering:
    *   Similarity calculations for different data types.
    *   Correct application of Ethical Weights.
    *   Score aggregation and normalization logic.
    *   Handling of missing data / sparse profiles.
    *   Generation of correct `traceability_data` structure.
    *   Edge cases and boundary conditions.
    *   Include specific ethical test cases as per [AI Ethical Testing Guide](./ai/ai_ethical_testing_guide.md) (e.g.,

testing fairness across simulated profiles).

*   **Documentation:** Use docstrings, inline comments. Update this guide and relevant specs. Use [Code Docs

Template](../../templates/code_documentation_template.md).

*   **Verification System:** Design for auditability. Log algorithm runs and key parameters used via the VS audit API.

Respond appropriately to VS bias flags if implemented.

*   **Performance:** Optimize calculations, especially for large user bases. Consider caching strategies for Value

Profile features if computation is heavy. Use efficient data structures.

*   **Ethical Review:** Submit significant changes to algorithm logic or weighting for ethical review.

* --

This algorithm is central to ThinkAlike's value proposition. Its development requires careful attention to both
technical performance and deep ethical alignment.
