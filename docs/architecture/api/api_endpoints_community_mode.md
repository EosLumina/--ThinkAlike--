# Api Endpoints - Project Backend - Community Mode

**Document Purpose:**

This document specifies the **API endpoints for the ThinkAlike project backend, specifically for Community Mode functionality.**  It is a supplementary document to the main `API_ENDPOINTS.md` and outlines the routes, methods, request/response formats, authentication requirements, and functionality of endpoints related to community creation, management, membership, and features within Community Mode.  Refer to `API_ENDPOINTS.md` for general API conventions, authentication details, and base URL information.

**I.  Base URL and Authentication:**

Refer to the main `API_ENDPOINTS.md` document for the Base URL and general Authentication information (JWT Bearer tokens).  All endpoints in this document, unless explicitly stated otherwise, **require JWT authentication**.

**II. API Endpoints - Community Mode Functionality:**

These endpoints are organized by Community Mode features:

**A. Community Creation and Discovery Endpoints (`/api/communities`)**

* `GET /api/communities`
  * **Purpose:** Get a list of public communities for directory display and community discovery.
  * **Method:** GET
  * **Authentication:** Optional (public directory view)
  * **Query Parameters (Optional):**
    * `search`: "string" -  Search communities by name or description.
    * `values`: "string (comma-separated ValueNode IDs)" - Filter communities by specific values.
    * `sortBy`: "enum ['members', 'creationDate', 'valueAlignment', ...]" - Sort communities by different criteria.
    * `page`: "integer" - Page number for pagination.
    * `pageSize`: "integer" - Number of communities per page.
  * **Response (200 OK, JSON):** Paginated list of CommunityProfile summaries:

        ```json
        {
          "communities": [
            {
              "communityId": "UUID",
              "communityName": "string",
              "tagline": "string",
              "description": "string (truncated)",
              "values": [ ... ], // Array of ValueNode IDs representing community values
              "memberCount": "integer",
              "profileImageUrl": "URL (optional)",
              // ... other summary community profile fields
            },
            // ... more community summaries
          ],
          "totalCount": "integer (total number of communities matching criteria)",
          "currentPage": "integer",
          "totalPages": "integer"
        }
        ```

  * **Error Responses:** (Standard error responses - see `API_ENDPOINTS.md`)
* `POST /api/communities`
  * **Purpose:** Create a new community.
  * **Method:** POST
  * **Authentication:** Required
  * **Request Body (JSON):** Community creation data:

        ```json
        {
          "communityName": "string (required)",
          "description": "string (required)",
          "tagline": "string (optional)",
          "values": [ "ValueNodeId1", "ValueNodeId2", ... ], // Array of ValueNode IDs
          "guidelines": "string (optional, community guidelines text)",
          "privacySettings": "enum ['public', 'private'] (required)",
          "governanceModel": "enum ['informal', 'direct_democracy', 'liquid_democracy', 'hybrid'] (required)",
          "profileImageUrl": "URL (optional)"
          // ... other community creation fields
        }
        ```

  * **Response (201 Created, JSON):** CommunityProfile data of newly created community.
  * **Error Responses:** 401 Unauthorized, 400 Bad Request (validation errors)

**B. Community Profile Endpoints (`/api/communities/{communityId}`)**

* `GET /api/communities/{communityId}`
  * **Purpose:** Get full profile data for a specific community.
  * **Method:** GET
  * **Authentication:** Optional (public profile view for public communities, member-authenticated for private communities)
  * **Response (200 OK, JSON):** CommunityProfile data (see Data Model in Community Mode Spec).
  * **Error Responses:** 404 Not Found, 401 Unauthorized (for private communities if not member)
* `PUT /api/communities/{communityId}`
  * **Purpose:** Update community profile data (for community administrators only).
  * **Method:** PUT
  * **Authentication:** Required (Admin authentication - to be specified - likely role-based authorization)
  * **Request Body (JSON):**  Partial CommunityProfile data with updates (admin-editable fields).
  * **Response (200 OK, JSON):** Updated CommunityProfile data.
  * **Error Responses:** 401 Unauthorized (if not admin), 403 Forbidden (if not authorized), 400 Bad Request (validation errors), 404 Not Found
* `DELETE /api/communities/{communityId}`
  * **Purpose:** Delete a community (for community creators/administrators only).
  * **Method:** DELETE
  * **Authentication:** Required (Creator/Admin authentication - to be specified)
  * **Response (200 OK, JSON):**

        ```json
        {
          "message": "Community deleted successfully"
        }
        ```

  * **Error Responses:** 401 Unauthorized (if not creator/admin), 403 Forbidden (if not authorized), 404 Not Found

**C. Community Membership Endpoints (`/api/communities/{communityId}/members`)**

* `GET /api/communities/{communityId}/members`
  * **Purpose:** Get a list of members for a specific community.
  * **Method:** GET
  * **Authentication:** Required (Member authentication - to view members of a community)
  * **Query Parameters (Optional):**
    * `search`: "string" - Search members by username or profile information.
    * `sortBy`: "enum ['joinDate', 'username', ...]" - Sort members by different criteria.
    * `page`: "integer" - Page number for pagination.
    * `pageSize`: "integer" - Number of members per page.
  * **Response (200 OK, JSON):** Paginated list of UserProfile summaries for community members:

        ```json
        {
          "members": [
            {
              "userId": "UUID",
              "username": "string",
              "profileImageUrl": "URL (optional)",
              "joinDate": "Timestamp",
              // ... other summary member profile fields
            },
            // ... more member summaries
          ],
          "totalCount": "integer (total number of members)",
          "currentPage": "integer",
          "totalPages": "integer"
        }
        ```

  * **Error Responses:** 401 Unauthorized (if not member), 404 Not Found
* `POST /api/communities/{communityId}/join`
  * **Purpose:** User requests to join a community (for public or private communities - triggers approval for private).
  * **Method:** POST
  * **Authentication:** Required
  * **Response (200 OK, JSON):**

        ```json
        {
          "message": "Membership request submitted successfully (or user joined community)"
        }
        ```

  * **Error Responses:** 401 Unauthorized, 404 Not Found, 409 Conflict (already a member or pending request)
* `POST /api/communities/{communityId}/leave`
  * **Purpose:** User leaves a community.
  * **Method:** POST
  * **Authentication:** Required (Member authentication)
  * **Response (200 OK, JSON):**

        ```json
        {
          "message": "Successfully left community"
        }
        ```

  * **Error Responses:** 401 Unauthorized, 404 Not Found (community or membership not found), 400 Bad Request (not a member)

**D. Community Management Endpoints (`/api/communities/{communityId}/admin`)** *(Admin-Authenticated)*

*(These endpoints require Administrator-level authentication within the specific community - Role-Based Access Control to be specified)*

* `GET /api/communities/{communityId}/admin/membership-requests`
  * **Purpose:** Get a list of pending membership requests for a private community (for community administrators).
  * **Method:** GET
  * **Authentication:** Required (Admin authentication)
  * **Response (200 OK, JSON):** Array of ConnectionRequest objects (or UserProfile summaries with request metadata)
  * **Error Responses:** 401 Unauthorized (if not admin), 403 Forbidden (if not authorized), 404 Not Found
* `POST /api/communities/{communityId}/admin/membership-requests/{requestId}/approve`
  * **Purpose:** Approve a pending membership request (for community administrators).
  * **Method:** POST
  * **Authentication:** Required (Admin authentication)
  * **Response (200 OK, JSON):**

        ```json
        {
          "message": "Membership request approved"
        }
        ```

  * **Error Responses:** 401 Unauthorized (if not admin), 403 Forbidden (if not authorized), 404 Not Found (request not found), 400 Bad Request (request already processed)
* `POST /api/communities/{communityId}/admin/membership-requests/{requestId}/decline`
  * **Purpose:** Decline a pending membership request (for community administrators).
  * **Method:** POST
  * **Authentication:** Required (Admin authentication)
  * **Response (200 OK, JSON):**

        ```json
        {
          "message": "Membership request declined"
        }
        ```

  * **Error Responses:** 401 Unauthorized (if not admin), 403 Forbidden (if not authorized), 404 Not Found (request not found), 400 Bad Request (request already processed)
* `DELETE /api/communities/{communityId}/admin/members/{membershipId}`
  * **Purpose:** Remove a member from a community (for community administrators/moderators - permissions to be defined).
  * **Method:** DELETE
  * **Authentication:** Required (Admin/Moderator authentication)
  * **Response (200 OK, JSON):**

        ```json
        {
          "message": "Member removed from community"
        }
        ```

  * **Error Responses:** 401 Unauthorized (if not admin/moderator), 403 Forbidden (if not authorized), 404 Not Found (membership not found)
* `(Further Admin Endpoints for Moderation, Governance Settings, etc. - to be specified as Community Mode features are further defined)`

**D. Community Forum Endpoints (`/api/communities/{communityId}/forums`)** *(Member-Authenticated)*

*(These endpoints require Member-level authentication within the specific community)*

* `GET /api/communities/{communityId}/forums`
  * **Purpose:** Get a list of forums within a community.
  * **Method:** GET
  * **Authentication:** Required (Member authentication)
  * **Response (200 OK, JSON):** Array of Forum objects (summary data - to be defined)
  * **Error Responses:** 401 Unauthorized (if not member), 404 Not Found
* `POST /api/communities/{communityId}/forums`
  * **Purpose:** Create a new forum within a community (Admin or member-permission based - to be defined).
  * **Method:** POST
  * **Authentication:** Required (Member or Admin authentication - permission-based)
  * **Request Body (JSON):** Forum creation data (name, description, permissions - if applicable)
  * **Response (201 Created, JSON):** Forum data of newly created forum.
  * **Error Responses:** 401 Unauthorized, 403 Forbidden (if not authorized), 400 Bad Request (validation errors), 404 Not Found

*(Further Forum Endpoints for Threads, Posts, etc. - to be specified as Forum features are further defined)*

**E. Direct/Liquid Democracy Endpoints (`/api/communities/{communityId}/governance`)** *(Optional - Community-Driven Implementation)*

*(These endpoints will be specified IF and WHEN Direct/Liquid Democracy tools are implemented in Community Mode, as these are optional, community-driven features)*

**F. Resource Sharing Endpoints (`/api/communities/{communityId}/resources`)** *(Member-Authenticated)*

*(Resource sharing endpoints will be specified as Resource Sharing features are further defined in Community Mode)*

**III. Data Models (Refer to Community Mode Specification):**

For detailed data model specifications for CommunityProfile, CommunityMembership, Forum, Resource, etc., please refer to the `docs/architecture/modes/community_mode/COMMUNITY_MODE_SPEC.md` document.

**IV. Error Handling and Response Codes:**

API endpoints will use standard HTTP status codes to indicate success or failure.  Refer to the main `API_ENDPOINTS.md` document for general error code definitions.

**V. Future Endpoints and Extensibility:**

This document represents the initial set of Community Mode API endpoints. Future endpoints will be added as Community Mode features evolve and expand, particularly for more detailed forum functionality, direct/liquid democracy tools, and resource sharing mechanisms.  All new Community Mode API endpoints will be documented in updated versions of this document.

---

---
**Document Details**
- Title: Api Endpoints - Project Backend - Community Mode
- Type: Architecture Documentation
- Version: 1.0.0
- Last Updated: 2025-04-05
---
End of Api Endpoints - Project Backend - Community Mode
---


