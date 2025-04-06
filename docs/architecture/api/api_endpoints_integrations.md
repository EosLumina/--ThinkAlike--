# API Endpoints - Backend - External Integrations

---

## 1. Introduction

This document specifies the **API endpoints for the ThinkAlike project backend related to integrating with third-party external services** (e.g., Goodreads, Spotify). It supplements the main [`API_ENDPOINTS.md`](api_endpoints.md) and details routes for managing OAuth connections, fetching data, and handling user consent specific to these integrations.

These endpoints support the features described in the [Data Integration Strategy](../data_integration_strategy.md) and are used by the [ConnectedServicesManager UI component](../../components/ui_components/connected_services_manager.md).

Refer to [`API_ENDPOINTS.md`](api_endpoints.md) for general API conventions, authentication details (JWT Bearer), base URL (`/api/v1`), and standard error response formats. All endpoints listed here require **Bearer Authentication** unless explicitly related to the OAuth callback phase which involves state validation.

---

## 2. API Endpoints - Integration Management

### 2.1 Connection Status & Configuration

*   `GET /api/v1/integrations/status`
    *   **Purpose:** Fetch the current connection status and configuration for all supported third-party services for the authenticated user.
    *   **Description:** Used by the `ConnectedServicesManager` UI component to display which services are connected, the permissions granted, and the user's current data usage consent settings for each service.
    *   **Method:** `GET`
    *   **Authentication:** Required.
    *   **Responses:**
        *   `200 OK`: Successfully retrieved integration statuses.
            ```json
            {
              "services": [
                {
                  "serviceId": "string (e.g., 'goodreads', 'spotify')",
                  "name": "string (e.g., 'Goodreads', 'Spotify')",
                  "isConnected": "boolean",
                  "permissionsGranted": ["string", "..."],
                  "usage": {
                    "matching": "boolean",
                    "community_recommendations": "boolean",
                    "profile_display": "boolean"
                  },
                  "lastSynced": "string (date-time, nullable)"
                }
              ]
            }
            ```
        *   `401 Unauthorized`: Authentication required.
        *   `500 Internal Server Error`: Error fetching status from database or configuration.

### 2.2 OAuth Flow Initiation & Callback

*   `GET /api/v1/integrations/{serviceId}/auth_url`
    *   **Purpose:** Get the external service's authorization URL to initiate the OAuth connection flow.
    *   **Description:** The frontend calls this endpoint when the user clicks "Connect". The backend generates the appropriate OAuth authorization URL for the specified service, including necessary parameters like `client_id`, `scope`, `redirect_uri`, and a unique `state` parameter (stored server-side in the user's session for CSRF protection).
    *   **Method:** `GET`
    *   **Authentication:** Required.
    *   **Path Parameters:**
        *   `serviceId` (string, required): Identifier of the service (e.g., 'goodreads', 'spotify').
    *   **Responses:**
        *   `200 OK`: Returns the authorization URL.
            ```json
            {
              "authUrl": "string (The full URL the frontend should redirect the user to)"
            }
            ```
        *   `400 Bad Request`: Invalid or unsupported `serviceId`.
        *   `401 Unauthorized`: Authentication required.
        *   `500 Internal Server Error`: Error generating state parameter or URL.

*   `GET /api/v1/integrations/{serviceId}/callback`
    *   **Purpose:** Handle the callback from the external OAuth provider after user authorization.
    *   **Description:** This is the `redirect_uri` registered with the third-party service. It receives the `code` (authorization code) and `state` from the provider. The backend validates the `state` parameter against the user's session, exchanges the `code` for access/refresh tokens, securely stores the tokens, and then typically redirects the user back to the frontend's "Connected Services" page.
    *   **Method:** `GET`
    *   **Authentication:** Implicitly linked to the user's session established *before* the redirect to the external service, primarily via the `state` parameter validation. Standard Bearer token not applicable here.
    *   **Path Parameters:**
        *   `serviceId` (string, required): Identifier of the service.
    *   **Query Parameters (from external service):**
        *   `code`: `string` (Authorization code).
        *   `state`: `string` (CSRF protection token to be validated against user session).
        *   `error`: `string` (Optional, if authorization failed on the provider side).
    *   **Responses:**
        *   `302 Found` (Redirect): On successful token exchange and storage, redirects the user back to a predefined frontend URL (e.g., `/settings/connected-services?success=true&service={serviceId}`).
        *   `400 Bad Request`: `state` mismatch (CSRF detected), missing `code`, invalid `serviceId`.
        *   `500 Internal Server Error`: Failed to exchange code for tokens with the external service, failed to store tokens securely. Error details should be logged securely, user sees a generic failure redirect (e.g., `/settings/connected-services?error=true&service={serviceId}`).

### 2.3 Connection Management & Consent

*   `PUT /api/v1/integrations/settings`
    *   **Purpose:** Update the user's data usage consent settings for one or more connected services.
    *   **Description:** Called by the frontend when a user toggles the data usage switches in the `ConnectedServicesManager` UI. Updates the user's preferences in the database.
    *   **Method:** `PUT`
    *   **Authentication:** Required.
    *   **Request Body (JSON):**
        ```json
        {
          "serviceId": "string (Required, e.g., 'goodreads')",
          "usage": {
            "matching": "boolean (optional)",
            "community_recommendations": "boolean (optional)",
            "profile_display": "boolean (optional)"
          }
        }
        ```
    *   **Responses:**
        *   `200 OK`: Settings updated successfully.
            ```json
            {
              "message": "Integration settings updated successfully.",
              "updatedService": {
                  "serviceId": "string",
                  "isConnected": true,
                  "permissionsGranted": ["..."],
                  "usage": { "matching": true, "community_recommendations": false, ... },
                  "lastSynced": "string (date-time, nullable)"
              }
            }
            ```
        *   `400 Bad Request`: Invalid input data (e.g., unknown `serviceId`, invalid usage keys).
        *   `401 Unauthorized`: Authentication required.
        *   `404 Not Found`: User does not have a connection for the specified `serviceId` to update settings for.
        *   `500 Internal Server Error`: Error saving settings to database.

*   `DELETE /api/v1/integrations/{serviceId}/connection`
    *   **Purpose:** Disconnect an external service and revoke ThinkAlike's access.
    *   **Description:** Called when the user clicks "Disconnect". The backend securely deletes stored tokens and associated harvested data for this service and user. It should also attempt to revoke the token with the third-party service if their API supports it.
    *   **Method:** `DELETE`
    *   **Authentication:** Required.
    *   **Path Parameters:**
        *   `serviceId` (string, required): Identifier of the service to disconnect.
    *   **Responses:**
        *   `204 No Content`: Successfully disconnected and data cleaned up.
        *   `401 Unauthorized`: Authentication required.
        *   `404 Not Found`: No active connection found for this user and service to disconnect.
        *   `500 Internal Server Error`: Error during token deletion, data cleanup, or revocation attempt.

### 2.4 Data Synchronization (Internal Trigger / Potential Manual Trigger)

*   `POST /api/v1/integrations/{serviceId}/sync`
    *   **Purpose:** Manually trigger a data synchronization task for a specific service for the authenticated user.
    *   **Description:** Primarily, data syncs run on a schedule or via background tasks. This endpoint provides an *optional* way for a user to request an immediate refresh via the UI (e.g., "Refresh My Goodreads Data" button). The backend should queue the sync task rather than executing it synchronously in the request.
    *   **Method:** `POST`
    *   **Authentication:** Required.
    *   **Path Parameters:**
        *   `serviceId` (string, required): Identifier of the service to sync.
    *   **Responses:**
        *   `202 Accepted`: Sync task successfully queued.
            ```json
            {
              "message": "Data synchronization task for {serviceId} has been queued.",
              "taskId": "string (Optional ID for the background task)"
            }
            ```
        *   `400 Bad Request`: Cannot queue sync (e.g., service not connected, sync already in progress).
        *   `401 Unauthorized`: Authentication required.
        *   `404 Not Found`: Service ID invalid or not connected.
        *   `500 Internal Server Error`: Error queuing the background task.

---

## 3. Data Models

*   **`UserExternalToken`**: Database model to store encrypted `access_token`, `refresh_token`, `expires_at`, `scopes_granted` per `user_id` and `service_name`.
*   **`UserIntegrationSetting`**: Database model/fields to store user consent toggles (`usage` flags like `matching`, `community_recommendations`) per `user_id` and `service_name`.
*   **`UserExternalData`**: Database model to store minimally processed, relevant data harvested from external services (e.g., list of book IDs/genres, top artist IDs/genres), linked to `user_id` and `service_name`, including `last_retrieved` timestamp.

*(Refer to [`unified_data_model_schema.md`](../../architecture/database/unified_data_model_schema.md) for detailed table definitions).*

---

## 4. Security & Error Handling

*   Emphasize secure handling and storage of OAuth tokens (encryption at rest).
*   Validate `state` parameter rigorously in OAuth callbacks to prevent CSRF.
*   Handle token expiry and refresh securely.
*   Enforce user consent checks *before* fetching or using external data.
*   Implement robust error handling for external API calls (timeouts, rate limits, permission errors).
*   Standard HTTP error codes used; error responses include `message`.

---
