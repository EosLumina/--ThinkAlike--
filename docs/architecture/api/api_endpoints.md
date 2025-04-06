// filepath: C:\--ThinkAlike--\docs\architecture\api\api_endpoints.md
# API Endpoints Reference

---

## 1. Introduction

Defines the available API endpoints and their usage.

---

## 1. Overview

# API Endpoints - ThinkAlike Platform

## 1. Introduction

This document provides a comprehensive specification of all API endpoints for the ThinkAlike platform backend. It details the request methods, URL paths, request/response formats, authentication requirements, and data validation procedures for each endpoint. This document is intended for frontend developers, backend engineers, and AI agents interacting with the ThinkAlike API. All API implementations are designed to adhere to the ethical data handling guidelines and transparency principles outlined in the [master reference](../../core/master_reference.md) document. Data traceability and UI-driven validation are integral components of each API workflow.

---

## 2. API Base URL

## 2. Endpoint Categories

**2.1 /users Resource & Authentication**

`https://api.thinkalike.example.com/api/v1`

*(Note: For local development, use `http://localhost:8000/api/v1` or similar)*

## 3. Authentication and Authorization

All API endpoints, unless explicitly stated otherwise, require **Bearer Authentication** using JWT (JSON Web Tokens). Authorization is role-based, with specific endpoints requiring appropriate user roles and privileges as detailed in the endpoint specifications below. UI components are designed to handle authentication workflows and to provide visual feedback to users regarding authentication status and access permissions.

## 4. API Endpoints

This section details each API endpoint, categorized by resource.

### 4.1 /users Resource & Authentication

* `POST /api/v1/auth/register`
  * **Purpose:** User registration / account creation.
  * **Method:** POST
  * **Request Body (JSON):**
  
    ```json
    {
      "username": "string (required, minLength: 3, maxLength: 30)",
      "email": "string (required, email format)",
      "password": "string (required, minLength: 8)",
      "full_name": "string (optional, maxLength: 100)"
    }
    ```

  * **Responses:**

    * `201 Created`: User account created successfully. Returns the new user's ID.

      ```json
      {
        "message": "User created successfully.",
        "user_id": "integer (The ID of the newly created user)",
        "user_data": {
          "type": "object",
          "description": "A set of data parameters for UI to validate successful user creation workflow with transparency and user control."
        }
      }
      ```

    * `400 Bad Request`: Invalid request data (e.g., missing fields, invalid email format, username already taken, password too short).

      ```json
      {
        "message": "Error message describing the invalid request data.",
        "ui_validation_components": {
           "type": "object",
           "description": "A set of reusable UI components that provide clear validation feedback to the user, highlighting data validity and security issues during the workflow."
        }
      }
      ```

    * `500 Internal Server Error`: Unexpected server error.

* `GET /api/v1/users/{userId}`
  * **Summary:** Retrieve user profile data by User ID.
  * **Description:** Retrieves comprehensive profile data for a specific user, identified by their User ID. Data is delivered through a secure and traceable data workflow implementation protocol, validated by UI components.
  * **Method:** `GET`
  * **Parameters:**
    * `userId` (path parameter, integer, required): The unique identifier of the user to retrieve.
  * **Authentication:** Bearer Authentication required. User might only be able to retrieve their own profile or profiles based on specific privacy settings/connections (Authorization logic applies).
  * **Responses:**

    * `200 OK`: Successful retrieval of user data.

      ```json
      {
        "user_id": "integer (Unique user ID, e.g., 123)",
        "username": "string (User's chosen username, e.g., johndoe)",
        "email": "string (User's email address, format: email, e.g., john.doe@example.com)",
        "full_name": "string (User's full name, optional, e.g., John Doe)",
        "profile_picture_url": "string (URL of profile picture, format: url, optional, e.g., /images/users/123.jpg)",
        "created_at": "string (Account creation timestamp, format: date-time, e.g., 2024-02-29T14:30:00Z)",
        "is_active": "boolean (Account status, e.g., true)",
        "bio": "string (User biography text, optional, e.g., 'Software developer passionate about ethical AI.')",
        "privacy_settings": {
          "profile_visibility": "string (Enum: public, private, connections_only, e.g., connections_only)",
          "type": "object",
          "description": "User's privacy settings."
        },
         "profile_data_extra": {
           "type": "object",
           "description": "Placeholder for other profile fields from Profiles table (birthdate, location, etc.) - Define structure based on Profiles table schema."
         }
        // Note: 'password_hash' is NEVER returned
      }
      ```

    * `401 Unauthorized`: Authentication token is missing or invalid.
    * `403 Forbidden`: Authenticated user does not have permission to view this profile.
    * `404 Not Found`: User with the specified `userId` not found.

*   `GET /api/v1/profiles/{userId}`
    *   **Summary:** Get user profile data (potentially redundant with `/users/{userId}`, decide which is primary).
    *   **Description:** Retrieves comprehensive profile data for a given user ID. Data is delivered through a clear, secure, and traceable data workflow implementation protocol, validated by UI components. *(Consider consolidating profile data retrieval into the `/users/{userId}` endpoint for simplicity unless there's a strong reason to keep separate endpoints).*
    *   **Method:** `GET`
    *   **Parameters:**
        *   `userId` (path parameter, integer, required): The unique identifier of the user to retrieve profile data for.
    *   **Authentication:** Bearer Authentication required. Authorization rules apply.
    *   **Responses:**
        *   `200 OK`: Returns user profile data. *(Response structure should be consistent with `GET /users/{userId}` if data is the same).*
            ```json
            {
              // Structure should ideally match the response of GET /users/{userId}
              // Including user_id, username, email, full_name, bio, birthdate, location, etc.
              "profile_data_from_get_profiles": {
                "type": "object",
                "description": "A comprehensive set of user profile parameters, accessible to the authenticated user for data exploration and validation within the UI. Ensure consistency with GET /users/{userId}."
              }
            }
            ```
        *   `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `500 Internal Server Error` (Similar to `GET /users/{userId}`).

**2.2 /communities Resource**

*   `POST /api/v1/communities`
    *   **Summary:** Create a community.
    *   **Description:** Creates a new community within the ThinkAlike platform, using data provided by the user and implementing clear data workflow protocols. Data workflows are rigorously tested through UI components to ensure transparency and user agency. Requires authentication.
    *   **Method:** `POST`
    *   **Request Body:** `application/json`
        ```json
        {
          "community_name": "string (required, unique)",
          "description": "string (required, text)",
          "tagline": "string (optional)",
          "values": ["string", "..."], // List of core value identifiers/tags
          "guidelines": "string (optional, text)",
          "privacy_settings": "string (required, enum: public, private)",
          "governance_model": "string (required, enum: informal, direct_democracy, ...)", // Refer to Community Mode spec
          "profile_image_url": "string (optional, url)"
          // Potentially 'creator_id' derived from authenticated user

```json
      {
        "message": "User not found.",
        "ui_feedback_components": {
           "type": "object",
           "description": "Reusable UI components providing clear error feedback to the user, validating data retrieval failures and system responses."
        }
      }
      ```

    * `500 Internal Server Error`: Unexpected server error.

* `PUT /api/v1/users/{userId}`
  * **Summary:** Update user profile data by User ID.
  * **Description:** Updates specific fields within a user's profile, identified by their User ID. This endpoint implements secure data modification protocols, with UI components providing data validation and workflow confirmation. Users can typically only update their own profile.
  * **Method:** `PUT`
  * **Parameters:**
    * `userId` (path parameter, integer, required): The unique identifier of the user profile to update.
  * **Request Body (JSON):** Include *only* the fields to be updated.

    ```json
    {
      "username": "string (optional, minLength: 3, maxLength: 30)",
      "email": "string (optional, email format)",
      "password": "string (optional, minLength: 8)", // For changing password
      "full_name": "string (optional, maxLength: 100)",
      "bio": "string (optional, maxLength: 500)",
      "privacy_settings": {
          "profile_visibility": "string (optional, enum: public, private, connections_only)"
      }
      // ... other updatable profile fields from Users/Profiles table
    }
    ```

**2.3 /match Resource**

* **Authentication:** Bearer Authentication required. User must typically match `{userId}`.
  * **Responses:**

    * `200 OK`: User profile updated successfully. May return the updated user profile data.

      ```json
      {
        "message": "User profile updated successfully.",
        // Optionally return updated user data similar to GET /users/{userId}
        "ui_validation": {
          "type": "object",
          "description": "UI components providing data validation feedback to confirm successful user profile update and data integrity within the workflow."
        }
      }
      ```

    * `400 Bad Request`: Invalid request data (e.g., invalid format, username taken).

**2.4 /interactions Resource**

*   `POST /api/v1/interactions`
    *   **Summary:** Record a user interaction event.
    *   **Description:** Records various types of user interactions (e.g., profile view, connection request, message sent, community action) with a clear data traceability workflow. Used for analytics, improving recommendations (ethically), and potentially moderation logs. UI components validate performance and ethical parameters.
    *   **Method:** `POST`
    *   **Request Body:** `application/json`
        ```json
        {
          "user_id": "integer (required, ID of the user performing the action - usually derived from token)",
          "target_user_id": "integer (optional, ID of the user being interacted with)",
          "target_community_id": "integer (optional, ID of the community involved)",
          "target_object_id": "string (optional, ID of specific content like post/message)",
          "interaction_type": "string (required, e.g., 'profile_view', 'connection_request_sent', 'message_sent', 'community_join', 'post_like', 'narrative_choice')",
          "interaction_data": { // Optional, context-dependent details
            "type": "object",
            "description": "Interaction details with specific validation schemas based on each UI element, ensuring data integrity and traceability.",
            // Example for 'narrative_choice': { "node_id": "xyz", "choice_made": "option_a" }
            // Example for 'message_sent': { "message_length": 120 } // Avoid logging message content here for privacy
          }

```json
      {
        "message": "Error message describing invalid request data.",
         "ui_validation_components": {
           "type": "object",
           "description": "Reusable UI components providing clear error feedback based on data validation failures, guiding users to correct input and workflow implementation."
        }
      }
      ```

    * `401 Unauthorized`: Authentication token is missing or invalid.
    * `403 Forbidden`: Authenticated user does not have permission to update this profile.
    * `404 Not Found`: User with the specified `userId` not found.

**2.5 /location Resource**

*   `POST /api/v1/location/share_live`
    *   **Summary:** Initiates a live location sharing session with a specified user or group.
    *   **Description:** Allows users to share their live location for a specified duration with a recipient (user or group). Implements secure data sharing protocols and provides UI components for workflow validation and user confirmation.
    *   **Method:** `POST`
    *   **Request Body (JSON):**
        ```json
        {
          "recipientId": "string (ID of user or group to share with)",
          "durationMinutes": "integer (Time in minutes for sharing to remain active)",
          "message": "string (Optional message to accompany sharing request)"

```json
      {
        "message": "User not found.",
        "ui_feedback_components": {
           "type": "object",
           "description": "Reusable UI components providing clear error feedback to the user."
        }
      }
      ```

    * `500 Internal Server Error`: Unexpected server error.

* `DELETE /api/v1/users/{userId}`
  * **Summary:** Delete a user account by User ID.
  * **Description:** Deletes a specific user profile and associated account, identified by User ID. Implements secure data deletion protocols and provides UI components for workflow validation and user confirmation. Requires careful authorization.
  * **Method:** `DELETE`
  * **Parameters:**
    * `userId` (path parameter, integer, required): The unique identifier of the user account to delete.
  * **Authentication:** Bearer Authentication required. Requires specific privileges (e.g., user deleting their own account after confirmation, or an administrator role).
  * **Responses:**

    * `200 OK` or `204 No Content`: User account deleted successfully.

      ```json
      // Optional 200 OK Body:
      {
        "message": "User deleted successfully.",
        "ui_validation": {
           "type": "object",
           "description": "UI components providing confirmation message and data validation feedback, highlighting the successful deletion of user data and the security workflow implementation process."
        }
      }
      ```

    * `401 Unauthorized`: Authentication token is missing or invalid.
    * `403 Forbidden`: Authenticated user does not have permission to delete this account.
    * `404 Not Found`: User with the specified `userId` not found.

      ```json
      {
        "message": "User not found.",
        "ui_feedback_components": {
           "type": "object",
           "description": "Reusable UI components providing clear error feedback to the user."
        }
      }
      ```

    * `500 Internal Server Error`: Unexpected server error.

**3. Components (OpenAPI/Swagger Style)**

* `POST /api/v1/profiles/{userId}/video`
  * **Summary:** Upload a video profile for a user.
  * **Description:** Enables users to upload a short video profile intro, enhancing profile authenticity and used for AI Clone generation. Implements secure data handling and transfer protocols, with UI components providing data validation and workflow feedback.
  * **Method:** `POST`
  * **Parameters:**
    * `userId` (path parameter, integer, required): The unique identifier of the user uploading the video. Must match authenticated user.
  * **Request Body:** `multipart/form-data`
    * Requires a form field named `video` containing the video file data (e.g., `.mp4`, `.webm`). Content-Type should be appropriate (e.g., `video/mp4`). Server-side validation for file size, type, and duration is essential.
  * **Authentication:** Bearer Authentication required. User must match `{userId}`.
  * **Responses:**

    * `201 Created`: Video profile uploaded successfully. May return the URL of the stored video.

      ```json
      {
        "message": "Video uploaded successfully.",
        "video_url": "string (URL where the video is stored)",
        "ui_validation": {
           "type": "object",
           "description": "UI components providing data validation and data transformation feedback, showcasing the workflow process with clear and actionable UI elements."
        }
      }
      ```

    * `400 Bad Request`: Invalid request data (e.g., missing file, wrong file type, file too large, security workflow failure).

      ```json
      {
        "message": "Error message describing invalid request data or security workflow failure.",
        "ui_validation_components": {
           "type": "object",
           "description": "Reusable UI components providing clear error feedback with specific details about data validity or security workflow issues, guiding users to correct input and workflow implementation."
        }
      }
      ```

    * `401 Unauthorized`: Authentication token is missing or invalid.
    * `403 Forbidden`: User does not match `{userId}`.
    * `404 Not Found`: User with the specified `userId` not found.
    * `500 Internal Server Error`: Error during file processing or storage.

* `GET /api/v1/profiles/{userId}`
  * **Summary:** Get user profile data (potentially redundant with `/users/{userId}`, decide which is primary).
  * **Description:** Retrieves comprehensive profile data for a given user ID. Data is delivered through a clear, secure, and traceable data workflow implementation protocol, validated by UI components. *(Consider consolidating profile data retrieval into the `/users/{userId}` endpoint for simplicity unless there's a strong reason to keep separate endpoints).*
  * **Method:** `GET`
  * **Parameters:**
    * `userId` (path parameter, integer, required): The unique identifier of the user to retrieve profile data for.
  * **Authentication:** Bearer Authentication required. Authorization rules apply.
  * **Responses:**
    * `200 OK`: Returns user profile data. *(Response structure should be consistent with `GET /users/{userId}` if data is the same).*

      ```json
      {
        // Structure should ideally match the response of GET /users/{userId}
        // Including user_id, username, email, full_name, bio, birthdate, location, etc.
        "profile_data_from_get_profiles": {
          "type": "object",
          "description": "A comprehensive set of user profile parameters, accessible to the authenticated user for data exploration and validation within the UI. Ensure consistency with GET /users/{userId}."
        }
      }
      ```

    * `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `500 Internal Server Error` (Similar to `GET /users/{userId}`).

## 5. Components (OpenAPI/Swagger Style)

The API specification is maintained in a separate specification file rather than being inline Markdown. The snippet below shows the security scheme definition which is consistent.

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

**4. Data Models (Detailed Data Schemas)**

## 6. Data Models (Detailed Data Schemas)

Schema definitions are documented separately in the following files or sections:

* **Matching Mode:**
  Refer to the endpoint specifications above for inline examples. See also:
  `docs/architecture/modes/matching_mode/matching_mode_spec.md`
  for the UserProfile (expanded), ValueProfile, Connection, and ConnectionRequest models.

* **Narrative Mode:**
  See:
  `docs/architecture/modes/narrative_mode/narrative_mode_spec.md`

* **Community Mode:**
  See:
  `docs/architecture/modes/community_mode/community_mode_spec.md`
  for the CommunityProfile, CommunityMembership, Forum, and Resource models.

* **Verification System:**
  See:
  `docs/architecture/verification_system/verification_system_data_models.md`
  for the AuditLogEntry, AlgorithmVerificationStatus, and TraceableProcess models.

* **Database Schema (Comprehensive):**
  Refer to:
  `docs/architecture/database/unified_data_model_schema.md`.

**5. Future Endpoints and Extensibility**

This document represents the initial set of API endpoints. Future endpoints will be added for more granular community features (forums, posts, governance actions), advanced matching functionalities, detailed verification system interactions, notifications, and potential external integrations. The API is designed for modularity and extensibility. Updates will be reflected in revised versions of this document and potentially within a formal OpenAPI specification.

**6. Revision History**

## 7. Future Endpoints and Extensibility

This document represents the initial set of API endpoints. Future endpoints will be added for more granular community features (forums, posts, governance actions), advanced matching functionalities, detailed verification system interactions, notifications, and potential external integrations. The API is designed for modularity and extensibility. Updates will be reflected in revised versions of this document and potentially within a formal OpenAPI specification.

## 8. Revision History

To maintain the accuracy and relevance of this API specification as the ThinkAlike platform evolves, this Revision History section will track significant updates and modifications made to this document over time. Please refer to this section to understand the changes and ensure you are always working with the latest version of the API specification.

Version | Date | Author | Description of Changes
------- | ---- | ------ | ---------------------
1.0 | March 26, 2025 | Eos Lumina | Initial Draft Creation - Comprehensive specification of API Endpoints for Users, Narrative, Matching, and Communities Resources. Includes base URL, authentication details, endpoint specifications, and initial component definitions. Establishes document as the "Source of Truth" for ThinkAlike API.

---
**Document Details**
- Title: API Endpoints Reference
- Type: Technical Documentation
- Version: 1.0.0
- Last Updated: 2025-04-05
---
End of API Endpoints Reference
---




