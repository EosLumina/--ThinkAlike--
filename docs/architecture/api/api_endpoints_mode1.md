# API Endpoints - Mode 1: Narrative Onboarding & Match Reveal

---

## 1. Introduction

This document specifies the **API endpoints for the ThinkAlike project backend, specifically for Mode 1 (Narrative Onboarding & Match Reveal) functionality.** It supplements the main `API_ENDPOINTS.md` and details the routes, methods, request/response formats, authentication, and functionality required to drive the interactive "Whispering Woods" choose-your-own-adventure experience. This mode serves as the primary onboarding mechanism, introduces core project values, elicits initial user Value Profile data, and culminates in a potential AI-driven "perfect match" reveal.

Refer to [`API_ENDPOINTS.md`](../api/api_endpoints.md) for general API conventions, authentication details (JWT Bearer), base URL (`/api/v1`), and standard error response formats. All endpoints listed here require **Bearer Authentication**.

These endpoints facilitate the stateful progression through the narrative, interaction with the AI Narrative Engine, and the final match reveal based on the user's choices.

---

## 2. API Endpoints - Mode 1 Functionality

### 2.1 Narrative Flow Management

* `GET /api/v1/narrative/start`
  * **Purpose:** Initiate a new Mode 1 narrative ("Whispering Woods") or resume an existing session for the authenticated user.
  * **Description:** Retrieves the starting narrative node (scene description, initial prompt, first choices) for a user beginning Mode 1, or fetches their last saved position if they left mid-adventure. This is the entry point for the Mode 1 experience.
  * **Method:** `GET`
  * **Authentication:** Required.
  * **Responses:**
    * `200 OK`: Successfully retrieved the starting or current narrative state.

            ```json
            {
              "narrativeNode": { // The current step/scene data
                "nodeId": "string (Unique ID for this narrative step/scene, e.g., 'ww_intro_1')",
                "nodeType": "string (Enum: 'prompt', 'scene_description', 'choice_point', 'match_reveal', 'narrative_end')",
                "content": {
                  "text": "string (Narrative text, AI agent dialogue, question)",
                  "imageUrl": "string (Optional URL for background/scene image)",
                  "audioUrl": "string (Optional URL for ambient sound/narration)"
                },
                "choices": [ // Array of choices if nodeType is 'choice_point'
                  {
                    "choiceId": "string (Unique ID for this choice, e.g., 'ww_intro_1_choice_a')",
                    "text": "string (Text displayed for the user's choice option)"
                    // "value_implication" field removed - backend infers value from choiceId
                  }
                  // ... more choices
                ],
                "isEnding": "boolean (True if this node represents an end state of the narrative flow)",
                "matchData": null // Typically null unless nodeType is 'match_reveal'
              },
              "sessionState": { // Identifier for the current narrative session/state
                  "sessionId": "string (Unique ID for this specific narrative playthrough)",
                  "progressPercentage": "float (Estimate of narrative completion, 0.0 to 1.0)" // Optional
              },
              "ui_feedback_components": {
                   "type": "object",
                   "description": "UI components confirming successful narrative state retrieval."
              }
            }
            ```

    * `401 Unauthorized`: Authentication required.
    * `404 Not Found`: Narrative definition unavailable or user state error.
    * `500 Internal Server Error`: Backend or AI Narrative Engine error retrieving state.

* `POST /api/v1/narrative/choice`
  * **Purpose:** Submit the user's selected choice for the current narrative step and retrieve the subsequent step or outcome.
  * **Description:** The core interaction endpoint for Mode 1. The frontend sends the `choiceId` selected by the user for the `currentNodeId` within the active `sessionId`. The backend interacts with the AI Narrative Engine and the matching logic to determine the next narrative state (including potential updates to the user's implicit Value Profile) and returns the corresponding `narrativeNode`. This endpoint drives the story forward and the underlying matching calculation.
  * **Method:** `POST`
  * **Authentication:** Required.
  * **Request Body (JSON):**

        ```json
        {
          "sessionId": "string (Required, identifier for the ongoing narrative playthrough)",
          "currentNodeId": "string (Required, ID of the node the user just responded to)",
          "chosenChoiceId": "string (Required, ID of the choice the user selected)"
        }
        ```

  * **Responses:**
    * `200 OK`: Choice successfully processed. Returns the next narrative state, which might be another step or the final match reveal.

            ```json
            // --- If narrative continues ---
            {
              "narrativeNode": { // The *next* step in the narrative
                "nodeId": "string",
                "nodeType": "string (e.g., 'prompt', 'choice_point')",
                "content": { "...": "..." },
                "choices": [ /* ... */ ], // If applicable
                "isEnding": "boolean (false)",
                "matchData": null
              },
              "sessionState": { // Updated session state
                  "sessionId": "string",
                  "progressPercentage": "float"
              },
              "ui_feedback_components": {
                   "type": "object",
                   "description": "UI components validating successful choice processing."
              }
            }
            // --- If narrative ends with MATCH REVEAL ---
            {
              "narrativeNode": {
                "nodeId": "string (e.g., 'ww_match_reveal')",
                "nodeType": "string ('match_reveal')",
                "content": {
                    "text": "string (Narrative text revealing the match, e.g., 'Through the clearing, you see a figure whose values resonate strongly with yours...')",
                    "imageUrl": "string (Optional image)"
                 },
                "choices": [], // No further choices at this point
                "isEnding": "boolean (true)",
                "matchData": { // Details of the revealed match
                    "matchedUserId": "integer",
                    "matchingPercentage": "float (The final calculated score)",
                    "keySharedValues": ["string", "..."], // Highlighted shared values
                    "aiCloneData": { // Data to render the AI Clone of the match
                        "videoIntroUrl": "string",
                        "styleParameters": {}
                    },
                    "connectionUnlocked": "boolean (True if direct connection is now enabled)"
                }
              },
              "sessionState": { // Final session state
                  "sessionId": "string",
                  "progressPercentage": 1.0
              },
              "ui_feedback_components": {
                   "type": "object",
                   "description": "UI components validating the successful match reveal."
              }
            }
            // --- If narrative ends WITHOUT a sufficient match ---
            {
              "narrativeNode": {
                "nodeId": "string (e.g., 'ww_end_no_match')",
                "nodeType": "string ('narrative_end')",
                "content": {
                  "text": "string (Concluding text, e.g., 'Your journey through the woods concludes for now. Continue exploring connections in Mode 2.')"
                },
                "choices": [],
                "isEnding": "boolean (true)",
                "matchData": null
              },
              "sessionState": { // Final session state
                  "sessionId": "string",
                  "progressPercentage": 1.0
              },
              "ui_feedback_components": {
                 "type": "object",
                 "description": "UI components indicating narrative completion without immediate match."
              }
            }
            ```

    * `400 Bad Request`: Invalid input (e.g., invalid `chosenChoiceId` for `currentNodeId`, invalid `sessionId`).

            ```json
             {
               "message": "Invalid choice or session state for narrative progression.",
               "ui_validation_components": {
                  "type": "object",
                  "description": "UI components providing feedback on invalid input."
               }
             }
            ```

    * `401 Unauthorized`: Authentication required.
    * `404 Not Found`: Narrative definition error (`currentNodeId` has no path for `chosenChoiceId`).
    * `409 Conflict`: Invalid session state or sequence error.
    * `500 Internal Server Error`: Error in backend logic, AI Narrative Engine, or matching calculation during choice processing.

---

## 3. Data Models

* **`NarrativeNode`**: Represents a single step/scene in the Mode 1 interactive narrative. Key fields: `nodeId`, `nodeType`, `content`, `choices`, `isEnding`, `matchData`. See structure in `GET /start` response. Note `matchData` is populated only on the final reveal node.
* **`NarrativeChoice`**: Represents a selectable option within a `choice_point` node. Key fields: `choiceId`, `text`. The associated *value implication* is handled by the backend logic/AI based on the `choiceId`.
* **`NarrativeSessionState`**: Contains identifiers (`sessionId`) and potentially progress indicators needed to maintain the user's state through the narrative flow.
* **`MatchRevealData`**: Structure containing details of the revealed "perfect match" if the narrative path and matching score threshold are met. Key fields: `matchedUserId`, `matchingPercentage`, `keySharedValues`, `aiCloneData`, `connectionUnlocked`.

*(Refer to the Mode 1 Spec (`mode1_narrative_onboarding_spec.md`) for more detailed conceptual data models if needed)*.

---

## 4. Error Handling

Standard HTTP error codes (400, 401, 404, 409, 500) are used. Error responses should follow the standard format including `message` and potentially `ui_validation_components`. `409 Conflict` might indicate trying to submit a choice for an already completed session.

---

## 5. Key Considerations for Mode 1 API

* **State Management:** The backend needs robust state management for each user's `NarrativeSessionState`.
* **AI Integration:** Endpoints need to efficiently interact with the AI Narrative Engine to get subsequent nodes based on choices and potentially update the underlying (implicit) Value Profile used by the matching algorithm.
* **Matching Logic Trigger:** The logic determining if/when the `match_reveal` node is returned (based on accumulated choices and matching score) resides in the backend, triggered during the processing of `POST /narrative/choice`.
* **Idempotency:** Consider if `POST /narrative/choice` needs to be idempotent in case of network retries (though typically advancing state isn't idempotent). Session state management should handle potential replays gracefully.

---

---
**Document Details**
- Title: API Endpoints - Mode 1: Narrative Onboarding & Match Reveal
- Type: API Documentation
- Version: 1.0.0
- Last Updated: 2025-04-05
---
End of API Endpoints - Mode 1: Narrative Onboarding & Match Reveal
---
````markdown



