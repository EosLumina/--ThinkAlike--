# API Endpoints Reference

## 1. Introduction

Defines the available API endpoints and their usage.

## 2. API Base URL

`https://api.thinkalike.example.com/api/v1`

*(Note: For local development, use `http://localhost:8000/api/v1` or similar.)*

## 3. Endpoint Categories

### 3.1 /users Resource & Authentication

- `POST /api/v1/auth/register`
  - **Purpose:** User registration / account creation.
- `GET /api/v1/users/{userId}`
  - **Summary:** Retrieve user profile data by User ID.

## 4. Authentication and Authorization

All API endpoints, unless explicitly stated otherwise, require **Bearer Authentication** using JWT (JSON Web Tokens). Authorization is role-based, with specific endpoints requiring appropriate user roles and privileges as detailed in the endpoint specifications below. UI components are designed to handle authentication workflows and to provide visual feedback to users regarding authentication status and access permissions.

## 5. API Endpoints

This section details each API endpoint, categorized by resource.

### 5.1 /users Resource & Authentication

- `POST /api/v1/auth/register`
  - **Purpose:** User registration / account creation.
  - **Method:** POST
  - **Request Body (JSON):**

    ```json
    {
      "username": "string (required, minLength: 3, maxLength: 30)",
      "email": "string (required, email format)",
      "password": "string (required, minLength: 8)",
      "full_name": "string (optional, maxLength: 100)"
    }
    ```

  - **Responses:**

    - `201 Created`: User account created successfully. Returns the new user's ID.

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

    - `400 Bad Request`: Invalid request data (e.g., missing fields, invalid email format, username already taken, password too short).

      ```json
      {
        "message": "Error message describing the invalid request data.",
        "ui_validation_components": {
           "type": "object",
           "description": "A set of reusable UI components that provide clear validation feedback to the user, highlighting data validity and security issues during the workflow."
        }
      }
      ```

    - `500 Internal Server Error`: Unexpected server error.

- `GET /api/v1/users/{userId}`
  - **Summary:** Retrieve user profile data by User ID.
  - **Description:** Retrieves comprehensive profile data for a specific user, identified by their User ID. Data is delivered through a secure and traceable data workflow implementation protocol, validated by UI components.
  - **Method:** `GET`
  - **Parameters:**
    - `userId` (path parameter, integer, required): The unique identifier of the user to retrieve.
  - **Authentication:** Bearer Authentication required. User might only be able to retrieve their own profile or profiles based on specific privacy settings/connections (Authorization logic applies).
  - **Responses:**

    - `200 OK`: Successful retrieval of user data.

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

    - `401 Unauthorized`: Authentication token is missing or invalid.
    - `403 Forbidden`: Authenticated user does not have permission to view this profile.
    - `404 Not Found`: User with the specified `userId` not found.

- `GET /api/v1/profiles/{userId}`
  - **Summary:** Get user profile data (potentially redundant with `/users/{userId}`, decide which is primary).
  - **Description:** Retrieves comprehensive profile data for a given user ID. Data is delivered through a clear, secure, and traceable data workflow implementation protocol, validated by UI components. *(Consider consolidating profile data retrieval into the `/users/{userId}` endpoint for simplicity unless there's a strong reason to keep separate endpoints).*
  - **Method:** `GET`
  - **Parameters:**
    - `userId` (path parameter, integer, required): The unique identifier of the user to retrieve profile data for.
  - **Authentication:** Bearer Authentication required. Authorization rules apply.
  - **Responses:**
    - `200 OK`: Returns user profile data. *(Response structure should be consistent with `GET /users/{userId}` if data is the same).*
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

## 6. Revision History

To maintain the accuracy and relevance of this API specification as the ThinkAlike platform evolves, this Revision History section will track significant updates and modifications made to this document over time. Please refer to this section to understand the changes and ensure you are always working with the latest version of the API specification.

Version | Date | Author | Description of Changes
------- | ---- | ------ | ---------------------
1.0 | March 26, 2025 | Eos Lumina | Initial Draft Creation - Comprehensive specification of API Endpoints for Users, Narrative, Matching, and Communities Resources. Includes base URL, authentication details, endpoint specifications, and initial component definitions. Establishes document as the "Source of Truth" for ThinkAlike API.

---
**Document Details**
- Title: API Endpoints Reference
- Type: API Documentation
- Version: 1.0.0
- Last Updated: 2025-04-06
---




