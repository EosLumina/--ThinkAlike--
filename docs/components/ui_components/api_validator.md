# Design Document: APIValidator UI Component

---

## 1. Introduction and Description

The **APIValidator** is a reusable React UI component designed to provide **transparent feedback on interactions between the ThinkAlike frontend and its backend API endpoints**. It serves as a key element of the **"UI as Validation Framework"**, intercepting or receiving data about API calls and displaying their status, request details, response data, and validation results directly within the UI during development, testing, or in specific diagnostic contexts.

Its primary purposes are to:

* **Demystify Backend Communication:** Make the process of API communication visible and understandable.
* **Validate Data Flow:** Confirm that data sent to the API meets expectations and that responses are correctly structured.
* **Aid Debugging:** Provide immediate insights into API call success/failure, request payloads, and response bodies.
* **Enhance Transparency:** Offer, in controlled scenarios, users a window into how their actions trigger backend processes.
* **Integrate with Testing:** Serve as a target for assertions in automated UI tests and provide visual confirmation during manual testing.

This component supports the testing and validation strategies outlined in the [Testing and Validation Plan](../../guides/developer_guides/testing_and_validation_plan.md) and the data flow transparency goals in the [Technical Specification Guide](../../guides/developer_guides/technical_specification_guide.md).

---

## 2. UI Components / Elements

The `APIValidator` component can be rendered in different contexts:

### 2.1 Status Indicator

* **Purpose:** Displays the immediate success or failure state of the API call.

* **UI Elements:**
  * **Icon/Color:** Uses simple icons (✅/❌/⏳) and color coding
    
    * Green for success (2xx status)
    * Red for errors (4xx/5xx)
    * Yellow/Orange for in progress or redirects (3xx/pending)
  
  * **Text:** Concise status text (e.g., "OK", "Error", "Pending", "Created").

### 2.2 Request Details (Collapsible/Expandable)

* **Purpose:** Show the data sent to the API.

* **UI Elements:**
  * Endpoint URL and HTTP method
  * Optionally, key request headers (with sensitive values masked)
  * Pretty-printed JSON payload (with sensitive fields masked)

### 2.3 Response Details (Collapsible/Expandable)

* **Purpose:** Display the data received from the API.

* **UI Elements:**
  * HTTP status code display
  * Optionally, response headers
  * Pretty-printed JSON response body
  * Frontend validation results (if available), with a link to a `DataValidationError` component when needed

### 2.4 Timestamp & Duration

* **Purpose:** Provide timing context for the API call.

* **UI Elements:**
  * Display of request initiation time
  * Duration until response (in milliseconds)

---

## 3. Data Flow and Interaction

1. **Trigger:** A UI action (e.g., button click) initiates an API call via a service function.
2. **Interception/Wrapping:** The API service function (or its wrapper around fetch/axios) records the request details before sending the call and captures the response/error after completion.
3. **State Update:** Captured data such as endpoint, method, payload, response code, response body, duration, and validation status are passed to the `APIValidator` via props or shared state.
4. **Rendering:** The component renders the relevant sections (Status, Request Details, Response Details, and Timing) with collapsible controls.
5. **Display Context:**

   * Globally in a developer console panel (logging recent API calls)
   * Locally, near the triggering element (e.g., as a toast notification)

---

## 4. Mermaid Diagram of Data Flow

```mermaid
graph TD
    A[UI Action (e.g., Button Click)] --> B{API Service Function Call};
    B -- Request Details Captured --> C[APIValidator State];
    B -- Sends Request --> D[Backend API Endpoint];
    D -- Sends Response --> B;
    B -- Response/Error Captured --> C;
    C -- Props/Context Update --> E(APIValidator Component);
    E -- Renders --> F[Visual Feedback in UI];
```

---

## 5. Code Implementation Notes

**Framework:** React

**Data Capture:**

Create a wrapper function around standard fetch or axios instances to record request details, execute the API call, capture response/error details (with timing), optionally perform frontend validation, and then update the shared state or pass data via props.

**State Management:**

* Use the Context API or a state management library for a global log.
* For local display, component state or props can be used.

**Component Structure (Conceptual Example):**

```jsx
import React, { useState } from 'react';
import StatusIcon from './StatusIcon'; // Reusable icon
// Import masking utilities

function APIValidator({ apiCallData }) {
  const [showRequest, setShowRequest] = useState(false);
  const [showResponse, setShowResponse] = useState(false);

  if (!apiCallData) return null; // Don't render if no data

  const {
    endpoint, method, requestPayload, responseStatus,
    responseBody, duration, timestamp, frontendValidationStatus
  } = apiCallData;

  // Basic masking - replace with a robust utility
  const maskSensitive = (data) => JSON.stringify(data, (key, value) =>
      ['password', 'token', 'secret'].includes(key.toLowerCase()) ? '***MASKED***' : value, 2);

  return (
    <div className={`api-validator status-${responseStatus >= 400 ? 'error' :
      (responseStatus >= 200 && responseStatus < 300 ? 'success' : 'info')}`}>
      <div className="api-summary">
        {/* <StatusIcon status={responseStatus} /> */}
        <span>{method} {endpoint}</span>
        <span>({responseStatus})</span>
        <span>[{duration}ms]</span>
        <button onClick={() => setShowRequest(!showRequest)}>
          {showRequest ? 'Hide Req' : 'Show Req'}
        </button>
        <button onClick={() => setShowResponse(!showResponse)}>
          {showResponse ? 'Hide Res' : 'Show Res'}
        </button>
      </div>

      {showRequest && (
        <div className="api-details request-details">
          <strong>Request:</strong>
          <pre><code>{maskSensitive(requestPayload)}</code></pre>
          {/* Optional Headers */}
        </div>
      )}

      {showResponse && (
        <div className="api-details response-details">
          <strong>Response:</strong>
          {frontendValidationStatus && <span>Validation: {frontendValidationStatus}</span>}
          <pre><code>{maskSensitive(responseBody)}</code></pre>
          {/* Optional Headers */}
        </div>
      )}
    </div>
  );
}

export default APIValidator;
```

**Masking:**

Implement robust utility functions for masking sensitive data (e.g., passwords, tokens, PII) in both request and response displays. This example uses a basic function.

**Configuration:**

Allow customization (e.g., via props or context) for default visibility of details, masking level, and whether the component is active.

---

## 6. Testing Instructions

* **Successful Call:**

  * Mock a successful API call (2xx status).
  * Verify that APIValidator displays a green status, correct endpoint/method, masked request payload, valid response body, and accurate timing.

* **Client Error Call:**

  * Mock a client error (4xx status).
  * Verify red status, proper error code, and relevant request/response details.

* **Server Error Call:**

  * Mock a server error (5xx status).
  * Verify red status, correct code, and a generic error message.

* **Data Validation (Frontend):**

  * Mock a successful API call but with response data failing frontend validation.
  * Verify that the API status is green but also displays the frontend validation failure.

* **Masking:**

  * Verify sensitive fields (e.g., passwords, tokens) are correctly masked (displayed as ***MASKED***).

* **Expand/Collapse:**

  * Ensure the "Show/Hide Req/Res" buttons toggle the details sections.

* **Performance:**

  * Render multiple APIValidator instances and verify the UI remains responsive.

---

## 7. Dependencies & Integration

* **Depends On:**

  * API service wrapper/interceptor function.
  * Global state or prop drilling mechanism for `apiCallData`.
  * Utility for masking sensitive data.
  * Reusable StatusIcon component (optional).
  * [ThinkAlike Style Guide](../../guides/developer_guides/style_guide.md) for colors and styles.

* **Integrates With:**

  * Any UI component that triggers an API call.
  * Developer Tools panel (for global logging).
  * Potentially the DataValidationError component for detailed error displays.
  * Automated UI testing frameworks (e.g., Cypress, Playwright).

---

## 8. Future Enhancements

* Filtering/Searching within a global API log.
* Copy-to-clipboard functionality for request/response data.
* More sophisticated integration for data validation display.
* Option to replay specific API calls (for debugging).
* Integration with backend tracing IDs for end-to-end request tracking.

