# API ENDPOINTS - ThinkAlike Project Backend - Verification System

**Document Purpose:**

This document specifies the **API endpoints for the ThinkAlike project backend, specifically for the Verification System.**  It is a supplementary document to the main `API_ENDPOINTS.md` and outlines the routes, methods, request/response formats, authentication requirements, and functionality of endpoints related to the Verification System's operations.  Refer to `API_ENDPOINTS.md` for general API conventions, authentication details, and base URL information.

**I.  Base URL and Authentication:**

Refer to the main `API_ENDPOINTS.md` document for the Base URL and general Authentication information (JWT Bearer tokens).  All endpoints in this document, unless explicitly stated otherwise, **require JWT authentication with appropriate administrative privileges** for accessing verification-related information and functionalities.  Access control and authorization levels for Verification System endpoints will be further detailed in the Security Considerations document.

**II. API Endpoints - Verification System Functionality:**

These endpoints are organized by the core functionalities of the Verification System:

**A. Ethical Guideline Endpoints (`/api/verification/guidelines`)** *(Admin-Authenticated)*

* `GET /api/verification/guidelines`
  * **Purpose:** Get a list of all Ethical Guidelines defined in the system.
  * **Method:** GET
  * **Authentication:** Required (Admin authentication - Verification System management privileges)
  * **Response (200 OK, JSON):** Array of Ethical Guideline objects:

        ```json
        [
          {
            "guidelineId": "UUID",
            "guidelineName": "string (e.g., 'User Privacy')",
            "guidelineDescription": "string (detailed description of the guideline)",
            "principleArea": "enum ['user_sovereignty', 'transparency', 'ethical_humanism', ...]", // Categorization by Enlightenment 2.0 principle
            "status": "enum ['active', 'draft', 'deprecated']",
            "lastUpdated": "Timestamp",
            // ... other guideline metadata
          },
          // ... more guideline objects
        ]
        ```

  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 500 Internal Server Error
* `GET /api/verification/guidelines/{guidelineId}`
  * **Purpose:** Get details for a specific Ethical Guideline.
  * **Method:** GET
  * **Authentication:** Required (Admin authentication - Verification System management privileges)
  * **Response (200 OK, JSON):** Detailed Ethical Guideline object (same format as in list response).
  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 404 Not Found, 500 Internal Server Error
  * *(Potentially Admin endpoints for managing guidelines - POST, PUT, DELETE - to be specified if guideline management via API is needed)*

**B. Algorithm Verification Endpoints (`/api/verification/algorithms`)** *(Admin-Authenticated)*

* `GET /api/verification/algorithms`
  * **Purpose:** Get a list of algorithms under verification (initially primarily the Matching Algorithm, but can be expanded).
  * **Method:** GET
  * **Authentication:** Required (Admin authentication - Verification System management privileges)
  * **Response (200 OK, JSON):** Array of AlgorithmVerificationStatus objects:

        ```json
        [
          {
            "algorithmId": "UUID (identifying the algorithm, e.g., 'value_based_matching_v1')",
            "algorithmName": "string (e.g., 'Value-Based Matching Algorithm')",
            "verificationStatus": "enum ['pending', 'in_progress', 'verified', 'failed_verification']",
            "lastVerificationDate": "Timestamp (last verification attempt)",
            "verifiedBy": "UserId (UUID of verifying admin - optional)",
            // ... other verification status metadata
          },
          // ... more algorithm verification status objects
        ]
        ```

  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 500 Internal Server Error
* `GET /api/verification/algorithms/{algorithmId}`
  * **Purpose:** Get detailed verification status and information for a specific algorithm.
  * **Method:** GET
  * **Authentication:** Required (Admin authentication - Verification System management privileges)
  * **Response (200 OK, JSON):** AlgorithmVerificationDetails object:

        ```json
        {
          "algorithmId": "UUID",
          "algorithmName": "string",
          "verificationStatus": "enum",
          "lastVerificationDate": "Timestamp",
          "verifiedBy": "UserId",
          "ethicalRationaleDocumentLink": "URL (link to document explaining ethical rationale)",
          "auditLogsLink": "URL (link to audit log entries for this algorithm)",
          "relatedGuidelines": [ ... ], // Array of EthicalGuideline IDs relevant to this algorithm
          // ... other detailed verification information
        }
        ```

  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 404 Not Found, 500 Internal Server Error
* `GET /api/verification/algorithms/{algorithmId}/ethical-rationale`
  * **Purpose:** Get the documented ethical rationale for a specific algorithm.
  * **Method:** GET
  * **Authentication:** Required (Admin authentication - Verification System management privileges) - *Potentially Publicly Accessible in future for increased transparency*
  * **Response (200 OK, JSON):**

        ```json
        {
          "algorithmId": "UUID",
          "algorithmName": "string",
          "ethicalRationale": "string (detailed text explaining the ethical rationale)",
          "rationaleDocumentLink": "URL (link to full rationale document - optional)"
        }
        ```

  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 404 Not Found, 500 Internal Server Error
* `GET /api/verification/algorithms/{algorithmId}/audit-logs`
  * **Purpose:** Get audit logs for a specific algorithm (changes, verification attempts, reviews).
  * **Method:** GET
  * **Authentication:** Required (Admin authentication - Verification System management privileges)
  * **Response (200 OK, JSON):** Array of AuditLogEntry objects (related to the specified algorithm).
  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 404 Not Found, 500 Internal Server Error

**C. Data Traceability Endpoints (`/api/verification/datatraceability`)** *(Admin-Authenticated - Potentially User-Accessible for limited data in future)*

* `GET /api/verification/datatraceability/processes`
  * **Purpose:** Get a list of processes with data traceability implemented (e.g., Matching Algorithm, User Data Handling, etc.).
  * **Method:** GET
  * **Authentication:** Required (Admin authentication - Verification System management privileges) - *Potentially User-Accessible in future for limited process info*
  * **Response (200 OK, JSON):** Array of TraceableProcess objects:

        ```json
        [
          {
            "processId": "UUID (identifying the process, e.g., 'value_based_matching_process')",
            "processName": "string (e.g., 'Value-Based Matching Process')",
            "description": "string (brief description of the traceable process)",
            "dataFlowDiagramLink": "URL (link to data flow diagram - optional)",
            // ... other process metadata
          },
          // ... more traceable process objects
        ]
        ```

  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 500 Internal Server Error
* `GET /api/verification/datatraceability/processes/{processId}`
  * **Purpose:** Get detailed information and visualization data for a specific traceable process.
  * **Method:** GET
  * **Authentication:** Required (Admin authentication - Verification System management privileges) - *Potentially User-Accessible in future for limited data visualization*
  * **Response (200 OK, JSON):** TraceableProcessDetails object:

        ```json
        {
          "processId": "UUID",
          "processName": "string",
          "description": "string",
          "dataFlowDiagramLink": "URL",
          "visualizationData": {      // Data specifically formatted for DataTraceability.jsx component
            "nodes": [ ... ],       // Array of Node objects (representing data sources, algorithms, data transformations)
            "edges": [ ... ]        // Array of Edge objects (representing data flow paths)
          },
          // ... other detailed process information
        }
        ```

  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 404 Not Found, 500 Internal Server Error

**D. Audit Log Endpoints (`/api/verification/audit-logs`)** *(Admin-Authenticated)*

* `GET /api/verification/audit-logs`
  * **Purpose:** Get a general audit log of Verification System activities (admin-only access).
  * **Method:** GET
  * **Authentication:** Required (Admin authentication - Verification System management privileges)
  * **Query Parameters (Optional):**
    * `filterBy`: "enum ['guideline', 'algorithm', 'datatraceability', 'admin_actions', ...]" - Filter logs by category.
    * `sortBy`: "enum ['timestamp', 'adminUser', 'actionType', ...]" - Sort logs by different criteria.
    * `page`: "integer" - Page number for pagination.
    * `pageSize`: "integer" - Number of log entries per page.
  * **Response (200 OK, JSON):** Paginated list of AuditLogEntry objects:

        ```json
        {
          "auditLogs": [
            {
              "logId": "UUID",
              "timestamp": "Timestamp",
              "adminUser": "UserId (UUID of admin user performing action)",
              "actionType": "enum ['guideline_created', 'algorithm_verified', 'data_traceability_audited', '...', ]",
              "affectedObjectId": "UUID (ID of guideline, algorithm, etc. affected)",
              "description": "string (detailed description of the audit event)",
              // ... other audit log entry fields
            },
            // ... more audit log entries
          ],
          "totalCount": "integer (total number of log entries)",
          "currentPage": "integer",
          "totalPages": "integer"
        }
        ```

  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 500 Internal Server Error
* `GET /api/verification/audit-logs/{logId}`
  * **Purpose:** Get details for a specific audit log entry.
  * **Method:** GET
  * **Authentication:** Required (Admin authentication - Verification System management privileges)
  * **Response (200 OK, JSON):** Detailed AuditLogEntry object (same format as in list response).
  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 404 Not Found, 500 Internal Server Error

**E. Platform Verification Status Endpoints (`/api/verification/status`)** *(Potentially Publicly Accessible in Future for Transparency Reporting)*

* `GET /api/verification/status/platform`
  * **Purpose:** Get overall platform verification status summary (high-level overview of verified components).
  * **Method:** GET
  * **Authentication:** Required (Admin authentication initially) - *Potentially Publicly Accessible in future for transparency reporting*
  * **Response (200 OK, JSON):** PlatformVerificationStatusSummary object:

        ```json
        {
          "platformVerificationStatus": "enum ['verified', 'partially_verified', 'unverified']",
          "verifiedComponentCounts": {
            "ethicalGuidelines": "integer",
            "algorithms": "integer",
            "dataTraceabilityProcesses": "integer",
            // ... other verified component counts
          },
          "lastPlatformVerificationReportLink": "URL (link to a detailed platform verification report - optional)",
          // ... other summary status information
        }
        ```

  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 500 Internal Server Error
* `GET /api/verification/status/modes`
  * **Purpose:** Get verification status for each Mode (Narrative, Matching, Community).
  * **Method:** GET
  * **Authentication:** Required (Admin authentication initially) - *Potentially Publicly Accessible in future*
  * **Response (200 OK, JSON):** Array of ModeVerificationStatus objects:

        ```json
        [
          {
            "modeName": "string (e.g., 'Matching Mode')",
            "verificationStatus": "enum",
            "lastVerificationDate": "Timestamp",
            "verifiedFeatureCounts": {
              "algorithms": "integer",
              "dataTraceabilityFeatures": "integer",
              // ... other mode-specific verified feature counts
            },
            // ... other mode-specific verification status information
          },
          // ... more ModeVerificationStatus objects (for each Mode)
        ]
        ```

  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 500 Internal Server Error
* `GET /api/verification/status/algorithms`
  * **Purpose:** Get verification status for specific algorithms (detailed algorithm verification statuses).
  * **Method:** GET
  * **Authentication:** Required (Admin authentication initially) - *Potentially Publicly Accessible in future*
  * **Response (200 OK, JSON):** Array of AlgorithmVerificationStatus objects (detailed status for each verified algorithm - same format as GET /api/verification/algorithms).
  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 500 Internal Server Error

**III. Data Models (Refer to Verification System Specification):**

Data models for AuditLogEntry, AlgorithmVerificationStatus, TraceableProcess, etc., will be detailed in a separate `docs/architecture/verification_system/VERIFICATION_SYSTEM_SPEC.md` document (to be generated next, if needed, or incorporated into the main Verification System spec document).

**IV. Error Handling and Response Codes:**

API endpoints will use standard HTTP status codes to indicate success or failure.  Refer to the main `API_ENDPOINTS.md` document for general error code definitions.

**V. Future Endpoints and Extensibility:**

This document represents the initial set of Verification System API endpoints. Future endpoints may be added as the Verification System evolves and new verification functionalities are implemented, particularly for more granular verification of specific features, data handling practices, and community governance mechanisms.  All new Verification System API endpoints will be documented in updated versions of this document.

---
