# API Endpoints - Mode 2: User Discovery & Connection

## 1. Introduction

This document specifies the **API endpoints for the ThinkAlike project backend, specifically for Mode 2 (User Discovery
& Connection) functionality.** It supplements the main `API_ENDPOINTS.md` and details the routes, methods,
request/response formats, authentication, and functionality related to **user-driven browsing of potential matches (User
Nodes/AI Clones), viewing detailed profiles, and initiating/managing the Narrative Compatibility Tests** required before
direct connections are established in this Mode.

Refer to `API_ENDPOINTS.md` for general API conventions, authentication details (JWT Bearer), base URL (`/api/v1`), and
standard error response formats. All endpoints listed here require **Bearer Authentication**.

Mode 2 allows users to proactively explore the network based on Value Profiles and Matching Percentages, initiating
connections only after successfully navigating a narrative compatibility gate.

* --

## 2. API Endpoints - Mode 2 Functionality

### 2.1 User Network Discovery & Profile Viewing

* `GET /api/v1/discovery/network`
  * **Purpose:** Fetch potential matches (User Nodes) for the authenticated user to browse in the Mode 2 discovery

interface.
  * **Description:** Retrieves a list of other users, typically sorted or filterable by initial compatibility scores

(Matching Percentage), activity, or user-defined preferences. Includes essential data to render AI Clones and profile
summaries for the browsing experience.
  * **Method:** `GET`
  * **Authentication:** Required.
  * **Query Parameters (Optional):**
    * `sortBy`: `string` (e.g., `matching_percentage_desc`, `last_active_desc`, `distance_asc`) - Sorting criteria.
    * `filterByValue`: `string` (Comma-separated list of value IDs/tags).
    * `filterByInterest`: `string` (Comma-separated list of interest IDs/tags).
    * `minMatchPercentage`: `float` (e.g., `0.5`) - Minimum score filter.
    * `page`: `integer` (Default: 1) - Pagination page number.
    * `pageSize`: `integer` (Default: 20) - Results per page.
  * **Responses:**
    * `200 OK`: Successfully retrieved a paginated list of User Nodes for discovery.

            ```json

            {
              "users": [
                {
                  "userId": "integer",
                  "username": "string",
                  "aiCloneData": { // Essential for Mode 2 browsing view
                    "videoIntroUrl": "string (URL of the user's short video intro)",
                    "styleParameters": { // AI-derived parameters for visual style
                        "hue": "float", "saturation": "float", "brightness": "float",
                        "waveform_pattern": "string"
                     },
                     "dominantValues": ["string", "..."] // Values influencing style
                  },
                  "matchingPercentage": "float (Score relative to the requesting user)",
                  "profileSummary": { // Concise info for card view
                    "tagline": "string (Optional)",
                    "keyValues": ["string", "..."], // Top shared/prominent values
                    "keyInterests": ["string", "..."] // Top shared/prominent interests
                  },
                  "lastActive": "string (date-time, optional)"
                }
                // ... more user summaries
              ],
              "pagination": {
                "currentPage": "integer",
                "pageSize": "integer",
                "totalItems": "integer",
                "totalPages": "integer"
              },
              "ui_feedback_components": {
                "type": "object",
                "description": "UI components validating successful retrieval and display of user network for discovery."
              }
            }
            ```

    * `400 Bad Request`: Invalid query parameter format.
    * `401 Unauthorized`: Authentication required.
    * `500 Internal Server Error`: Error retrieving or processing user data.

* `GET /api/v1/discovery/profile/{userId}`
  * **Purpose:** Fetch detailed profile information for a specific user selected from the discovery network view.
  * **Description:** Retrieves comprehensive details needed for the full profile view in Mode 2, including video intro

URL, personal narrative, detailed values/interests, and the crucial `matchingPercentage` relative to the requesting
user. Access respects target user's privacy settings. *(Consistency check needed with `GET /users/{userId}` - ensure
this endpoint provides Mode 2 specific needs like `matchingPercentage` and potentially excludes sensitive data not
relevant for initial discovery).*
  * **Method:** `GET`
  * **Authentication:** Required.
  * **Parameters:**
    * `userId` (path parameter, integer, required): The ID of the user whose profile is being requested.
  * **Responses:**
    * `200 OK`: Successfully retrieved detailed profile data for Mode 2 display.

            ```json

            {
              // Core user fields (userId, username, etc. - ensure consistency)
              "userId": "integer",
              "username": "string",
              "aiCloneData": { // For displaying the clone/video on the profile page
                 "videoIntroUrl": "string",
                 "styleParameters": { "...":"..." }
              },
              "matchingPercentage": "float (Crucial: Score relative to the requesting user)",
              "personalNarrative": {
                  "content": "object or string", // User's self-authored narrative
                  "privacy": "string" // Reflects narrative visibility setting
               },
              "values": [ /* Array of user's detailed values */ ],
              "interests": [ /* Array of user's detailed interests */ ],
              "sharedCommunities": [ // Optional: Shared Mode 3 communities
                { "communityId": "integer", "communityName": "string" }
              ],
              "bio": "string (optional)",
              "full_name": "string (optional)", // Other relevant profile fields
              "ui_feedback_components": {
                "type": "object",
                "description": "UI components validating successful retrieval of detailed profile for Mode 2."
              }
            }
            ```

    * `401 Unauthorized`: Authentication required.
    * `403 Forbidden`: Requesting user does not have permission to view this detailed profile (privacy settings).
    * `404 Not Found`: User with the specified `userId` not found.
    * `500 Internal Server Error`: Error retrieving profile data.

### 2.2 Narrative Compatibility Test Management (Connection Gating)

* `POST /api/v1/connection/initiate_test`
  * **Purpose:** Initiate the Narrative Compatibility Test between the authenticated user (requester) and a target user.
  * **Description:** Triggered when the requester clicks "Connect" on a target user's profile in Mode 2. The backend

checks eligibility (not already connected, not blocked, no recent failed test) and starts a new test session, returning
the first narrative step. This acts as the gate before direct communication.
  * **Method:** `POST`
  * **Authentication:** Required.
  * **Request Body (JSON):**

        ```json

        {
          "targetUserId": "integer (Required, the ID of the user the requester wants to connect with)"
        }
        ```

  * **Responses:**
    * `201 Created`: Test session initiated successfully. Returns the starting narrative node for the requester.

            ```json

            {
              "message": "Narrative Compatibility Test initiated.",
              "testSessionId": "string (Unique ID for this specific test instance between users)",
              "narrativeNode": { // The first step of the compatibility narrative
                "nodeId": "string",
                "nodeType": "string (e.g., 'prompt', 'scene_description')",
                "content": { "text": "string", "imageUrl": "string (optional)" },
                "choices": [ { "choiceId": "string", "text": "string" } ] // Starting choices
              },
              "ui_feedback_components": {
                "type": "object",
                "description": "UI components validating successful test initiation."
              }
            }
            ```

    * `400 Bad Request`: Cannot initiate test (e.g., already connected, test in progress, requester/target ineligible).
    * `401 Unauthorized`: Authentication required.
    * `403 Forbidden`: Requesting user is blocked by the target user, or other permission issue.
    * `404 Not Found`: Target user `targetUserId` not found.
    * `409 Conflict`: A test between these users is already active or recently failed.
    * `500 Internal Server Error`: Error setting up the test session or generating the narrative.

* `POST /api/v1/connection/test/choice`
  * **Purpose:** Submit the user's choice within an ongoing Narrative Compatibility Test and get the next step or final

outcome.
  * **Description:** The user provides their choice for the current narrative step within the test session. The backend

(likely involving the AI Narrative Engine) processes this choice, potentially updates an internal compatibility score
for the test, and determines the next narrative node or the final outcome of the test (connection enabled or denied).
  * **Method:** `POST`
  * **Authentication:** Required.
  * **Request Body (JSON):**

        ```json

        {
          "testSessionId": "string (Required, identifier for the test instance)",
          "currentNodeId": "string (Required, ID of the node the user is responding to)",
          "chosenChoiceId": "string (Required, ID of the choice the user selected)"
        }
        ```

  * **Responses:**
    * `200 OK`: Choice processed. Returns either the next narrative node or the final outcome.

            ```json

            {
              "narrativeNode": { // EITHER this is present...
                "nodeId": "string",
                "nodeType": "string",
                "content": { "...": "..." },
                "choices": [ /* ... */ ],
                "isEnding": "boolean (false)"
              },
              "testOutcome": null, // ...OR narrativeNode is null and testOutcome is present
              "ui_feedback_components": {
                "type": "object",
                "description": "UI components validating choice processing."
              }
            }
            ```

            * OR (if the test concludes)*

            ```json

            {
              "narrativeNode": null, // Test ended
              "testOutcome": { // FINAL result
                "status": "string (Enum: 'connection_enabled', 'connection_denied')", // Outcome based on compatibility score threshold reached during test
                "finalMatchingPercentage": "float (Optional, the score calculated during the test)",
                "reason": "string (Optional, user-friendly reason if denied, e.g., 'Value alignment threshold not met during narrative.')",
                "message": "string (User-facing message for the outcome)"
              },
              "ui_feedback_components": {
                "type": "object",
                "description": "UI components validating the final test outcome."
              }
            }
            ```

    * `400 Bad Request`: Invalid input (`testSessionId`, `currentNodeId`, `chosenChoiceId`).
    * `401 Unauthorized`: Authentication required.
    * `404 Not Found`: `testSessionId` or `currentNodeId` not found.
    * `409 Conflict`: Test session already completed or state mismatch (e.g., wrong user trying to submit choice).
    * `500 Internal Server Error`: Error processing choice or determining outcome.

* (Endpoints for managing established connections themselves, like listing connections (`GET /connections`) or removing

them (`DELETE /connections/{connectionId}`), would likely reside under a general `/connections` resource defined in the
main `api_endpoints.md`, as they apply regardless of how the connection was formed).*

* --

## 3. Data Models

* **`UserNodeSummaryMode2`**: Data for discovery view (`userId`, `username`, `aiCloneData`, `matchingPercentage`,

`profileSummary`). See `GET /discovery/network`.

* **`AICloneData`**: Visual representation data (`videoIntroUrl`, `styleParameters`).
* **`DetailedUserProfileMode2`**: Profile data for detail view (`userId`, `username`, `aiCloneData`,

`matchingPercentage`, `personalNarrative`, values, interests, etc.). See `GET /discovery/profile/{userId}`.

* **`NarrativeCompatibilityTestSession`**: Backend state for an ongoing test (`testSessionId`, user IDs, current node,

score, history).

* **`NarrativeNode` / `NarrativeChoice` (Compatibility Test Variant)**: Structure similar to Mode 1 nodes/choices, but

content tailored for assessing compatibility between two specific users.

* **`TestOutcome`**: Final result of the compatibility test (`status`, `finalMatchingPercentage`, `reason`, `message`).

See `POST /connection/test/choice` response.

* (Refer to the Mode 2 Spec (`mode2_profile_discovery_spec.md`) and shared data models for detailed definitions).*

* --

## 4. Error Handling

Standard HTTP errors apply. Pay attention to:

* `403 Forbidden` for privacy/blocking issues,
* `404 Not Found` for missing users or sessions, and
* `409 Conflict` for invalid test states.

Error bodies include a `message` field and may also contain `ui_validation_components` for UI feedback.

* --

* --

## Document Details

* Title: API Endpoints - Mode 2: User Discovery & Connection

* Type: API Documentation

* Version: 1.0.0

## - Last Updated: 2025-04-05

End of API Endpoints - Mode 2: User Discovery & Connection
