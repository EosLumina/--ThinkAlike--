# Developer Guide: Value-Based Matching Algorithm

---

## 1. Introduction

This guide provides a comprehensive overview for developers working on the ThinkAlike **Value-Based Matching Algorithm**. This is a core component, primarily used in **Mode 2 (Profile Discovery)** for suggesting potential connections and gating interaction via Narrative Compatibility Tests, and potentially informing the "perfect match" reveal in **Mode 1 (Narrative Onboarding)**.

Its central purpose is to connect users based on **shared values and ethical alignment**, moving beyond superficial metrics. It implements **Ethical Weighting** and relies heavily on **Value Profiles**, always prioritizing **User Agency** and **Transparency**.

This guide details the algorithm's architecture, data inputs, ethical weighting logic, integration with the Verification System, and requirements for transparency via UI components like [DataTraceability](../components/ui/data_traceability.md). It adheres to principles in the [MASTER_REFERENCE.md](../core/master_reference.md) and [Ethical Guidelines](../core/ethics/ethical_guidelines.md).

## 2. Purpose and Goals

* **Identify Value-Aligned Connections:** Ethically identify potential connections based on compatibility derived from user **Value Profiles**.

* **Prioritize Ethical Congruence:** Implement **Ethical Weighting** to favor connections aligned with [Enlightenment 2.0 Principles](../core/enlightenment_2_0/enlightenment_2_0_principles.md).

* **Empower User Choice:** Provide transparent **Matching Percentages** and rationale (via DataTraceability) to inform user decisions.

* **Foster a Value-Driven Ecosystem:** Encourage connections grounded in shared ethical foundations.

## 3. Core Principles

* **Value-Centricity:** **Value Profiles** are the primary input. Shared ethics take precedence over superficial similarity.

* **Ethical Weighting:** Explicitly prioritize core ThinkAlike values in scoring.

* **Transparency & Explainability (XAI):** Logic, weights, and data flows are documented and designed for auditability ([Verification System Spec](../architecture/verification_system/verification_system.md)) and visualization ([DataTraceability Spec](../components/ui/data_traceability.md)). No black boxes.

* **User Control:** Users manage their Value Profiles and influence matching criteria via settings and feedback.

* **Data Privacy & Minimization:** Operates within the [Data Handling Policy](./data_handling_policy_guide.md) and uses the minimum necessary data ethically.

## 4. Algorithm Architecture and Data Flow (Backend Service)

The matching algorithm resides within a dedicated backend service (e.g., a `MatchingService` implemented with FastAPI).

### 4.1 Input Data: Value Profiles

The algorithm primarily consumes **Value Profiles**, constructed from:

* **Explicit Profile Data:** User-defined values and interests stored in the [Unified Data Model](../architecture/database/unified_data_model_schema.md).

* **Narrative-Derived Data (Mode 1):** Implicit values inferred from onboarding choices ([Mode 1 Spec](../architecture/modes/mode1_narrative_onboarding_spec.md)).

* **Consented External Data Insights:** Derived interests from connected services (e.g., Goodreads genres) via the [ConnectedServicesManager](../components/ui/connected_services_manager_spec.md) as described in the [Data Integration Strategy](../architecture/data_integration_strategy.md).

* **(Future) Interaction Data:** Aggregated, anonymized interaction patterns requiring further ethical design and consent.

### 4.2 Calculation: Ethically Weighted Similarity

The core logic compares two Value Profiles:

1. **Feature Extraction:** Identify and extract comparable features (e.g., common value tags, shared interests, narrative archetypes).
2. **Similarity Calculation:** Compute similarity for each feature category using measures such as the Jaccard index or cosine similarity.
3. **Ethical Weighting Application:** Multiply each similarity score by a pre-defined ethical weight:

    `WeightedScore_i = Similarity_i * EthicalWeight_i`

   Core ethical values (per [Ethical Guidelines](../core/ethics/ethical_guidelines.md)) receive higher weights.
4. **Aggregation:** Combine weighted scores into a final **Matching Percentage** (e.g., weighted average normalized to 0–100).
5. **Bias Check (Integration):** Optionally invoke the [Verification System API](../architecture/api/api_endpoints_verification_system.md) for fairness checks across demographic groups.

### 4.3 Output Data

Outputs are provided via API responses (e.g., for `POST /api/v1/match` or `GET /api/v1/discovery/network`):

* A list of `matchedUserId`s.

* A `matchingPercentage` score for each match.

* `sharedValues` or `keyFactors`: The top features contributing to the score.

* `traceability_data`: Structured data (nodes/edges) conforming to the expected input of the [DataTraceability](../components/ui/data_traceability.md) component, which visualizes the rationale behind the match.

## 5. Ethical Weighting Implementation

* **Taxonomy:** Define a clear taxonomy of values derived from [Enlightenment 2.0 Principles](../core/enlightenment_2_0/enlightenment_2_0_principles.md) and [Ethical Guidelines](../core/ethics/ethical_guidelines.md).

* **Weight Assignment:** Assign numerical weights (managed via configuration or the Verification System) with documented rationale.

* **Algorithm Logic:** Implement weighting within the scoring function, e.g., via weighted summation.

* **Transparency:** Clearly communicate the weighting approach to users, supported by visualization in [DataTraceability](../components/ui/data_traceability.md).

## 6. DataTraceability & Validation Integration

* **Traceability Output:** Produce comprehensive `traceability_data` detailing inputs, weighting steps, and results for visualization.

* **Explainability:** Use the generated `traceability_data` as the primary mechanism for explaining match rationale in the UI.

* **UI Validation:** Users verify that the [DataTraceability](../components/ui/data_traceability.md) graph aligns with their understanding.

* **Verification System:** Optionally log and audit runs, including bias checks if applicable.

## 7. Contribution Guidelines

* Adhere to our ["Perfect Coding" principles](../templates/code_documentation_template.md) and [Code Style Guide](../guides/developer_guides/code_style_guide.md).

* Write comprehensive unit tests (using Pytest) covering all aspects of the matching logic and edge cases.

* Document code thoroughly, especially the ethical weighting and traceability generation.

* Design for auditability and transparency through integration with the [Verification System](../architecture/verification_system/verification_system.md).

* Submit significant changes for ethical review before merging.

---
