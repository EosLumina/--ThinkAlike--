# ThinkAlike: Verification System Data Models

---

## 1. Introduction

This document defines the core data models (schemas) used by the ThinkAlike **Verification System**. These models represent the structure of data related to ethical guidelines, algorithm verification, data traceability, audit logging, and overall platform verification status.

These data models are essential for:

*   Structuring data returned by the Verification System API endpoints defined in [api_endpoints_verification_system.md](../api/api_endpoints_verification_system.md).
*   Providing a clear schema for data stored persistently (likely within the main platform database, e.g., PostgreSQL) but managed logically by the Verification System.
*   Ensuring consistency in how verification-related information is handled and represented throughout the platform.

These models are integral to the functioning of the Verification System as described in [verification_system.md](verification_system.md).

---

## 2. Core Data Models

### 2.1 EthicalGuideline

*   **Description:** Represents a single ethical guideline defined within the ThinkAlike framework, used for validating platform components and AI models.
*   **Fields:**
    *   `guidelineId` (UUID/String, Primary Key): Unique identifier for the guideline.
    *   `guidelineName` (String): Short, human-readable name of the guideline (e.g., "User Data Minimization", "Algorithmic Transparency").
    *   `guidelineDescription` (String/Text): Detailed explanation of the guideline's principle and intent.
    *   `principleArea` (Enum/String): Categorizes the guideline based on the core Enlightenment 2.0 principles (e.g., `user_sovereignty`, `transparency`, `ethical_humanism`, `positive_anarchism`, `authentic_connection`, `redefined_progress`).
    *   `status` (Enum/String): Current status of the guideline (e.g., `active`, `draft`, `deprecated`).
    *   `lastUpdated` (Timestamp): Date and time the guideline was last modified.
    *   `relatedComponents` (Array[String], Optional): List of platform components or features particularly relevant to this guideline.

### 2.2 AlgorithmVerificationStatus

*   **Description:** Represents the high-level verification status of a specific algorithm used within ThinkAlike (e.g., the Matching Algorithm).
*   **Fields:**
    *   `algorithmId` (UUID/String, Primary Key): Unique identifier for the algorithm instance/version being verified (e.g., `value_based_matching_v1.2`).
    *   `algorithmName` (String): Human-readable name of the algorithm (e.g., "Value-Based Matching Algorithm").
    *   `version` (String): Specific version identifier for the algorithm.
    *   `verificationStatus` (Enum/String): Current verification status (e.g., `pending`, `in_progress`, `verified`, `failed_verification`, `needs_review`).
    *   `lastVerificationDate` (Timestamp, Nullable): Date and time of the last verification attempt or success.
    *   `verifiedBy` (UUID/String, Nullable): Identifier of the admin user or system process that performed the last verification.
    *   `ethicalRationaleDocumentLink` (URL/String, Optional): Link to the detailed document explaining the algorithm's ethical design and rationale.
    *   `auditLogsLink` (URL/String, Optional): Link to related audit log entries for this specific algorithm.

### 2.3 AlgorithmVerificationDetails

*   **Description:** Provides more detailed information about the verification status and context of a specific algorithm, often including fields from `AlgorithmVerificationStatus`.
*   **Fields:**
    *   *(Inherits/Includes fields from `AlgorithmVerificationStatus`)*
    *   `ethicalRationaleSummary` (String/Text, Optional): A brief summary of the ethical rationale.
    *   `relatedGuidelines` (Array[UUID/String]): List of `guidelineId`s directly relevant to or checked against for this algorithm.
    *   `biasAssessmentResult` (Enum/String, Optional): Summary result of the latest bias assessment (e.g., `passed`, `warning`, `failed`).
    *   `transparencyScore` (Float/Integer, Optional): A quantitative or qualitative score representing the algorithm's explainability/transparency level.
    *   `latestAuditReportLink` (URL/String, Optional): Link to the most recent detailed audit report.
    *   `verificationHistory` (Array[Object], Optional): A list of past verification events (e.g., `{ timestamp: Timestamp, status: Enum, verifiedBy: UUID, notes: String }`).

### 2.4 TraceableProcess

*   **Description:** Represents a high-level business process or workflow within ThinkAlike for which data traceability is tracked and visualized.
*   **Fields:**
    *   `processId` (UUID/String, Primary Key): Unique identifier for the traceable process (e.g., `user_onboarding_mode1`, `value_matching_mode2`).
    *   `processName` (String): Human-readable name of the process (e.g., "User Onboarding Narrative", "Value-Based Matching Workflow").
    *   `description` (String/Text): Brief explanation of the process being traced.
    *   `dataFlowDiagramLink` (URL/String, Optional): Link to an external or generated visual diagram of the data flow.
    *   `lastTraceabilityAudit` (Timestamp, Nullable): Date of the last audit focusing on this process's traceability.

### 2.5 TraceableProcessDetails

*   **Description:** Provides detailed information for visualizing a specific traceable process, often including fields from `TraceableProcess`. This structure is designed to be directly consumable by UI components like `DataTraceability.jsx`.
*   **Fields:**
    *   *(Inherits/Includes fields from `TraceableProcess`)*
    *   `visualizationData` (JSON/Object): Data structured for graph visualization libraries.
        *   `nodes`: (Array[NodeObject]) - Represents data sources, processing steps, UI components, or data storage points.
            *   `id` (String/Number): Unique identifier within the graph.
            *   `label` (String): Display name for the node.
            *   `type` (Enum/String): Category of the node (e.g., `ui_component`, `api_endpoint`, `ai_model`, `database_table`, `data_source`).
            *   *(Other optional properties for styling/metadata)*
        *   `edges`: (Array[EdgeObject]) - Represents the flow of data between nodes.
            *   `source` (String/Number): ID of the source node.
            *   `target` (String/Number): ID of the target node.
            *   `label` (String, Optional): Description of the data or action being transferred.
            *   `dataType` (String, Optional): Type of data flowing along the edge.
            *   *(Other optional properties for styling/metadata, e.g., `isEncrypted`, `validationStatus`)*
    *   `relatedGuidelines` (Array[UUID/String], Optional): List of `guidelineId`s relevant to data handling within this process.

### 2.6 AuditLogEntry

*   **Description:** Represents a single entry in the Verification System's audit log, tracking significant actions related to ethical validation, configuration changes, or security events within the verification scope.
*   **Fields:**
    *   `logId` (UUID/String, Primary Key): Unique identifier for the log entry.
    *   `timestamp` (Timestamp): Date and time the action occurred.
    *   `adminUser` (UUID/String, Nullable): Identifier of the admin user performing the action (or 'system' if automated).
    *   `actionType` (Enum/String): Category of the action performed (e.g., `guideline_updated`, `algorithm_verified`, `verification_failed`, `data_traceability_audited`, `security_setting_changed`, `user_report_reviewed`).
    *   `affectedObjectType` (Enum/String, Nullable): Type of object affected by the action (e.g., `EthicalGuideline`, `Algorithm`, `TraceableProcess`, `User`, `Community`).
    *   `affectedObjectId` (UUID/String, Nullable): Identifier of the specific object affected.
    *   `description` (String/Text): Human-readable summary of the event.
    *   `details` (JSON/Object, Optional): Additional structured details about the event (e.g., specific changes made, parameters used).
    *   `ipAddress` (String, Optional): IP address associated with the action (use with privacy considerations).

### 2.7 PlatformVerificationStatusSummary

*   **Description:** Provides a high-level overview of the overall verification status of the entire ThinkAlike platform.
*   **Fields:**
    *   `platformVerificationStatus` (Enum/String): Overall status (e.g., `verified`, `partially_verified`, `unverified`, `needs_review`).
    *   `verifiedComponentCounts` (JSON/Object): Counts of verified components by type (e.g., `{ "ethicalGuidelines": 15, "algorithms": 2, "dataTraceabilityProcesses": 5 }`).
    *   `lastPlatformVerificationReportLink` (URL/String, Optional): Link to the latest comprehensive platform verification report.
    *   `lastCheckedTimestamp` (Timestamp): When this summary was last generated/updated.

### 2.8 ModeVerificationStatus

*   **Description:** Provides a verification status summary specific to one of ThinkAlike's core Modes (Narrative, Matching, Community).
*   **Fields:**
    *   `modeName` (String): Name of the Mode (e.g., "Narrative Mode", "Matching Mode", "Community Mode").
    *   `verificationStatus` (Enum/String): Overall status for this Mode (e.g., `verified`, `partially_verified`, `unverified`).
    *   `lastVerificationDate` (Timestamp, Nullable): Date of the last verification specific to this Mode.
    *   `verifiedFeatureCounts` (JSON/Object): Counts of verified features or sub-components within this Mode (e.g., `{ "algorithms": 1, "ui_workflows": 10, "data_handling_points": 25 }`).
    *   `modeSpecificReportLink` (URL/String, Optional): Link to a detailed verification report for this specific Mode.

---

## 3. Relationships

These data models are interconnected:

*   `AlgorithmVerificationDetails` references `EthicalGuideline` (`relatedGuidelines`).
*   `AuditLogEntry` references various objects (`affectedObjectId`) like `EthicalGuideline`, `AlgorithmVerificationStatus`, `TraceableProcess` based on `affectedObjectType`.
*   `TraceableProcessDetails` may reference `EthicalGuideline` (`relatedGuidelines`).
*   `PlatformVerificationStatusSummary` aggregates status information, potentially derived from `AlgorithmVerificationStatus`, `ModeVerificationStatus`, etc.
*   `ModeVerificationStatus` aggregates status information for components within a specific mode.

---

## 4. Storage Considerations

While logically part of the Verification System, these data models will likely be stored as tables or collections within the main ThinkAlike platform database (e.g., PostgreSQL) for operational efficiency. Appropriate indexing and access controls must be applied to ensure performance and security, restricting access primarily to the Verification System services and authorized administrative interfaces.

---
