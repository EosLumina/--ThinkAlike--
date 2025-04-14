# UI Component Specification: ConnectedServicesManager

---

## 1. Introduction and Description

The **ConnectedServicesManager** is a dedicated UI component, typically within user Settings, providing a centralized interface for users to manage connections to optional third-party services (e.g., Goodreads, Spotify). It is the primary UI for the [Third-Party Data Integration Strategy](../architecture/data_integration_strategy.md).

It allows users to view supported services, initiate/revoke OAuth connections, view granted permissions, and exercise **granular, opt-in control over how harvested data is used**, embodying user control and transparency principles. See [Connected Services User Guide](../guides/user_guides/connected_services_guide.md).

## 2. UI Elements and Layout

Renders as a panel listing services.

* **Service Listing Area:** List/grid of supported services. Each entry includes:

  * Service Icon/Logo & Name.

  * Connection Status ("Connected" / "Not Connected").

  * Action Button (`ActionButton`): "Connect" or "Disconnect".

  * Expand/Details Toggle (Optional).

* **Detailed Service View (Expanded):**

  * **Permissions Granted Display (`DataDisplay`):** Lists scopes granted via OAuth.

  * **Data Usage Toggles (`ToggleSwitch` / `Checkbox`):** **CRITICAL.** Granular, opt-in toggles for each potential use case (e.g., "Use for Matching?", "Use for Community Recs?", "Display on Profile?"). **Default OFF.** Changes trigger API saves.

  * **Last Synced Timestamp (`DataDisplay`).**

  * **View Harvested Data Link:** Navigates to `Data Explorer Panel` filtered by this service.

* **General Feedback Area (`Alert`):** Shows success/error messages for connect/disconnect/settings updates.

## 3. Data Flow and Interaction

Describes Load -> Connect -> Callback -> Panel Refresh -> Toggle Consent -> Disconnect -> Panel Refresh sequence. Can include a Mermaid diagram.

## 4. Code Implementation Notes

* **Framework:** React.

* **State:** Manages list of services, connection statuses, toggle states (fetched/updated via global state or local state with API calls).

* **Components:** Uses `ActionButton`, `ToggleSwitch`, `DataDisplay`, `Alert`.

* **API Interaction:** Calls backend endpoints for status (`GET /integrations/status`), auth URLs (`GET /integrations/{service}/auth_url`), settings updates (`PUT /integrations/settings`), disconnection (`DELETE /integrations/{service}/connection`). See [Integration API Docs](../architecture/api/api_endpoints_integrations.md). Handle loading/error states.

## 5. Testing Instructions

* Test initial load (states, errors).

* Test Connect flow (redirect, successful callback updates UI, failed callback shows error).

* Test Disconnect flow (confirmation, API call, UI update, error handling).

* Test toggling usage consent switches (API call, UI confirmation, state persistence after refresh).

* Test Permissions display accuracy based on mocked API data.

* Test Data Explorer link functionality.

* Test Accessibility (keyboard, screen reader).

## 6. UI Mockup Placeholder

* `[Placeholder: Link to ConnectedServicesManager mockup]`

## 7. Dependencies & Integration

* **Depends:** Backend Integration APIs, Reusable UI components, Global State (potentially), Style Guide.

* **Integrates:** User Settings/Profile section, `Data Explorer Panel` (via link).

## 8. Future Enhancements

* More detailed sync status/history, manual refresh trigger UI, bulk enable/disable, clearer permission explanations.
