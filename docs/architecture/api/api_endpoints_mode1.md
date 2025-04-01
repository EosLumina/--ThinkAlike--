# API ENDPOINTS - ThinkAlike Project Backend - Narrative Mode (Mode 1)

---

## 1. Introduction

This document specifies the **API endpoints for the ThinkAlike project backend, specifically for Narrative Mode (Mode 1) functionality.** It is a supplementary document to the main [`API_ENDPOINTS.md`](api_endpoints.md) and outlines the routes, methods, request/response formats, authentication requirements, and functionality of endpoints related to the interactive onboarding narrative, value elicitation, and initial AI-driven matching process within Mode 1.

Refer to [`API_ENDPOINTS.md`](api_endpoints.md) for general API conventions, authentication details (JWT Bearer), base URL (`/api/v1`), and standard error response formats. All endpoints listed here, unless otherwise specified, require **Bearer Authentication**.

Narrative Mode heavily relies on interaction with the **AI Narrative Engine** service via the backend API.

---

## 2. API Endpoints - Narrative Mode Functionality

### 2.1 Narrative Flow Management

*   `GET /api/v1/narrative/start`
    *   **Purpose:** Start a new Narrative Mode session or resume an existing one for the authenticated user.
    *   **Description:** Retrieves the initial narrative node (scene, prompt, choices) for a new user or fetches the user's last saved state to resume their "Whispering Woods" adventure. Used upon entering Mode 1.
    *   **Method:** `GET`
    *   **Authentication:** Required.
    *   **Responses:**
        *   `200 OK`: Successfully retrieved the current or starting narrative state.
            ```json
            {
              "narrativeNode": {
                  "nodeId": "string (Unique ID for this narrative step/scene)",
                  "nodeType": "string (Enum: 'prompt', 'scene_description', 'choice_point', 'match_reveal', ...)",
                  "content": {
                    "text": "string (Narrative text, question, or description displayed to user)",
                    "imageUrl": "string (Optional URL for scene image)",
                    "audioUrl": "string (Optional URL for background audio/narration)"
                  },
                  "choices": [
                      {
                        "choiceId": "string (Unique ID for this choice)",
                        "text": "string (Text representing the user's choice)",
                        "value_implication": "string (Optional hint about the value this choice represents)"
                      }
                      // ... other choices
                  ],
                  "isEnding": "boolean (Indicates if this is a concluding node)",
                  "matchData": {
                      "matchedUserId": "integer",
                      "aiCloneData": {
                          "videoIntroUrl": "string",
                          "styleParameters": {}
                      },
                      "initialMessage": "string (Optional introductory message)"
                  },
                  "ui_feedback_components": {
                     "type": "object",
                     "description": "Reusable UI components validating successful narrative state retrieval."
                  }
              },
              "sessionState": {
                  "type": "string",
                  "description": "Session identifier for the ongoing narrative."
              }
            }
            ```
        *   `401 Unauthorized`: Authentication required.
        *   `404 Not Found`: Narrative definition missing or user state corrupted.
        *   `500 Internal Server Error`: Backend or AI service error retrieving state.

*   `POST /api/v1/narrative/choice`
    *   **Purpose:** Submit the user's choice for the current narrative step and retrieve the next step.
    *   **Description:** The user selects an option from a `choice_point` node. The frontend sends the chosen `choiceId` along with the current `sessionState` to the backend. The backend processes the choice (updating user's implicit Value Profile, advancing narrative logic via the AI Narrative Engine) and returns the *next* `narrativeNode`.
    *   **Method:** `POST`
    *   **Authentication:** Required.
    *   **Request Body (JSON):**
        ```json
        {
          "sessionState": "string (Required, identifier from the previous step)",
          "currentNodeId": "string (Required, ID of the node the user is responding to)",
          "chosenChoiceId": "string (Required, ID of the choice the user selected)"
        }
        ```
    *   **Responses:**
        *   `200 OK`: Choice processed successfully, returning the next narrative state.
            ```json
            {
              "narrativeNode": {
                "nodeId": "string",
                "nodeType": "string",
                "content": { "...": "..." },
                "choices": [ /* ... */ ], // If the next node is a choice point
                "isEnding": "boolean",
                "matchData": { /* ... */ }, // If the next node is the match reveal
                "ui_feedback_components": {
                   "type": "object",
                   "description": "Reusable UI components validating successful choice processing and state transition."
                 }
              },
              "sessionState": {
                  "type": "string",
                  "description": "Updated session identifier."
              }
            }
            ```
        *   `400 Bad Request`: Invalid input (e.g., invalid `choiceId` for the `currentNodeId`, invalid `sessionState`).
            ```json
             {
               "message": "Invalid choice or session state.",
               "ui_validation_components": {
                  "type": "object",
                  "description": "UI components providing feedback on invalid input."
               }
             }
            ```
        *   `401 Unauthorized`: Authentication required.
        *   `404 Not Found`: Narrative path error, `currentNodeId` not found.
        *   `500 Internal Server Error`: Backend or AI service error processing choice or generating next state.

### 2.2 Narrative Data & Profile Interaction (Implicit)

Note: Explicit endpoints to *get* the narrative-derived value profile might exist under `/users/{userId}/profile` or similar, but the primary *update* happens implicitly via `POST /api/v1/narrative/choice`.

*   `GET /api/v1/narrative/user-narrative` (Potentially under `/users/me/narrative`)
    *   **Purpose:** Retrieve the user's completed or partially completed Personal Narrative content (distinct from the Mode 1 adventure flow state).
    *   **Description:** Allows users to view or edit the textual narrative they may construct as part of their profile, possibly influenced by or started during Mode 1.
    *   **Method:** `GET`
    *   **Authentication:** Required.
    *   **Responses:**
        *   `200 OK`: Returns the user's narrative content.
            ```json
            {
              "userId": "integer",
              "narrativeContent": {
                "type": "object", // Or string if simple text
                "description": "User-created narrative content, possibly structured JSON or Markdown.",
                "example": { "sections": [ { "title": "My Core Values", "text": "..." } ] }
              },
              "privacySettings": "string (Enum: public, private, connections_only)",
              "lastUpdated": "string (date-time)"
            }
            ```
        *   `401 Unauthorized`, `404 Not Found` (if no narrative created yet), `500 Internal Server Error`.

*   `PUT /api/v1/narrative/user-narrative` (Potentially under `/users/me/narrative`)
    *   **Purpose:** Update the user's Personal Narrative content.
    *   **Description:** Allows users to save changes to their textual narrative.
    *   **Method:** `PUT`
    *   **Authentication:** Required.
    *   **Request Body (JSON):**
        ```json
        {
          "narrativeContent": { /* Updated narrative content */ },
          "privacySettings": "string (Enum: public, private, connections_only)"
        }
        ```
    *   **Responses:**
        *   `200 OK`: Narrative updated successfully. May return the updated narrative.
        *   `400 Bad Request` (invalid data), `401 Unauthorized`, `500 Internal Server Error`.

---

## 3. Data Models

*   **`NarrativeNode`**: Represents a single step/scene in the interactive narrative. See structure in `GET /narrative/start` response. Key fields: `nodeId`, `nodeType`, `content`, `choices`, `isEnding`, `matchData`.
*   **`NarrativeChoice`**: Represents a user's option within a `choice_point` node. Key fields: `choiceId`, `text`, `value_implication`.
*   **`UserNarrativeContent`**: Represents the user's self-authored textual narrative (distinct from the Mode 1 adventure flow). See `GET /narrative/user-narrative` response.

*(Refer to specific Mode 1 specifications for more detailed data model definitions if needed).*

---

## 4. Error Handling

Standard HTTP error codes (400, 401, 403, 404, 500) are used. Error responses should include a `message` field and may include `ui_validation_components` or `ui_feedback_components` as defined in the main [`API_ENDPOINTS.md`](api_endpoints.md).

---

## 5. Future Endpoints

*   Endpoints for retrieving specific narrative definitions or metadata.
*   Endpoints allowing admins or developers to define/edit narrative flows.
*   Endpoints to reset or replay the narrative mode for a user.

---
