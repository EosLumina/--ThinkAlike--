# Practical Guide: Using the UI as Validation Framework

**Version:** 1.0
**Date:** March 26, 2025

---

## 1. Introduction

This guide provides practical examples demonstrating how developers should utilize ThinkAlike's specific **validation-focused UI components** during development and testing. These components are central to the **"UI as Validation Framework"** concept, embedding ethical guidelines, data schema checks, API contract adherence, and other rules directly into the application flow. They provide immediate, contextual feedback, accelerating development and ensuring the final product aligns with ThinkAlike's core principles.

Refer to the individual component specification documents in [`docs/components/ui_components/`](../../components/ui_components/) for detailed props, APIs, and implementation notes for each validation component mentioned here.

---

## 2. Example: Using `CoreValuesValidator` for Content Moderation Hints

* **Purpose:** To provide real-time feedback to users (and developers during testing) about whether their input aligns with community content guidelines or ethical principles *before* submission.
* **Component Spec:** [`docs/components/ui_components/CoreValuesValidator.md`](../../components/ui_components/CoreValuesValidator.md)
* **Scenario:** A user is writing a post in a Mode 3 Community Forum. We want to subtly check for potential violations of hate speech or overly aggressive language rules defined in the [`Ethical Guidelines`](../../core/ethics/ethical_guidelines.md).

* **Conceptual React Implementation:**

    ```jsx
    import React, { useState, useCallback, useMemo } from 'react';
    import CoreValuesValidator from '../../components/ui_components/CoreValuesValidator'; // Adjust import path
    import { ethicalRules } from '../../config/ethicsConfig'; // Assume rules are defined here

    function CommunityPostForm({ onSubmit }) {
      const [postContent, setPostContent] = useState('');
      const [validationStatus, setValidationStatus] = useState({ isValid: true, concerns: [] });

      // Define the specific rules to apply for this context
      const relevantRules = useMemo(() => [
        ethicalRules.content.noHateSpeech,
        ethicalRules.content.civilityTone
      ], []);

      // Callback to receive validation results from the component
      const handleValidationResult = useCallback((isValidResult, issues) => {
        setValidationStatus({ isValid: isValidResult, concerns: issues || [] });
      }, []);

      const handleSubmit = (event) => {
        event.preventDefault();
        if (validationStatus.isValid) {
          onSubmit(postContent);
          setPostContent(''); // Clear form on successful submit
          setValidationStatus({ isValid: true, concerns: [] }); // Reset validation
        } else {
          alert('Please review your post content based on the guidelines.');
        }
      };

      return (
        <form onSubmit={handleSubmit}>
          <label htmlFor="postContentInput">New Post:</label>
          <textarea
            id="postContentInput"
            value={postContent}
            onChange={(e) => setPostContent(e.target.value)}
            rows={8}
            aria-invalid={!validationStatus.isValid}
            aria-describedby="postValidationFeedback"
          />

          {/* Embed the validator - potentially debounced */}
          <CoreValuesValidator
            textToValidate={postContent}
            rules={relevantRules}
            onValidationResult={handleValidationResult}
            displayMode="compact" // Show only status/icons unless hovered/clicked
            debounceTimeout={750} // Validate slightly after user stops typing
          />

          {/* Display feedback based on validator's result */}
          <div id="postValidationFeedback" style={{ marginTop: '5px', minHeight: '20px' }}>
            {!validationStatus.isValid && validationStatus.concerns.length > 0 && (
              <span style={{ color: 'orange', fontSize: '0.9em' }}>
                {/* Use a specific warning icon */} ⚠️ Potential Guideline Issues: {validationStatus.concerns.join('; ')}
              </span>
            )}
            {/* Optionally show positive feedback when valid after typing */}
            {validationStatus.isValid && postContent.length > 10 && (
               <span style={{ color: 'green', fontSize: '0.9em' }}>✅ Looks good.</span>
            )}
          </div>

          <button type="submit" disabled={!validationStatus.isValid || postContent.trim().length === 0}>
            Submit Post
          </button>
        </form>
      );
    }

    export default CommunityPostForm;
    ```

* **Explanation:** The `CoreValuesValidator` is embedded directly within the form. As the user types (debounced), it validates the `postContent` against specific `ethicalRules`. The results (`isValid`, `issues`) are fed back to the parent form via the `onValidationResult` callback. The parent form then updates its state to display appropriate UI feedback (warnings, status messages) and controls the submit button's disabled state based on validation success. This provides an immediate, in-context ethical check.

---

## 3. Example: Using `APIValidator` in Development/Debug Mode

* **Purpose:** To transparently show developers the details of API requests and responses during development, helping to debug communication issues and validate data against schemas.
* **Component Spec:** [`docs/components/ui_components/APIValidator.md`](../../components/ui_components/APIValidator.md)
* **Scenario:** A developer is working on the user profile update feature and wants to see the exact payload sent to the backend and the response received, including validation status against an expected schema.

* **Conceptual Implementation (API Client Wrapper & Global Log):**

  * **API Client Wrapper (`apiClient.js` or similar):**

        ```javascript
        import axios from 'axios';
        import { apiValidationLogStore } from './stores/apiValidationLogStore'; // Example Zustand/Context store
        // import { schemas } from './config/apiSchemas'; // Assume schemas are available

        const apiClient = axios.create({
          baseURL: process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000/api/v1',
          // Other Axios config...
        });

        // Add interceptors ONLY in development mode
        if (process.env.NODE_ENV === 'development') {
          apiClient.interceptors.request.use(request => {
            const callData = {
              type: 'request',
              id: Date.now() + Math.random(), // Simple unique ID for the call
              timestamp: new Date().toISOString(),
              endpoint: request.url,
              method: request.method?.toUpperCase(),
              requestPayload: request.data,
              // Find relevant schema if available based on url/method
              // schema: schemas[request.url]?.[request.method?.toUpperCase()]?.request,
              status: 'pending'
            };
            apiValidationLogStore.getState().addLog(callData); // Add to global log store
            request.meta = { callId: callData.id }; // Pass ID to response interceptor
            return request;
          });

          apiClient.interceptors.response.use(response => {
             const startTime = response.config.meta?.startTime || Date.now(); // Need to set startTime in request interceptor ideally
             const duration = Date.now() - startTime;
             const callData = {
               type: 'response',
               id: response.config.meta?.callId,
               timestamp: new Date().toISOString(),
               endpoint: response.config.url,
               method: response.config.method?.toUpperCase(),
               responseStatus: response.status,
               responseBody: response.data,
               durationMs: duration,
               // Find relevant schema
               // schema: schemas[response.config.url]?.[response.config.method?.toUpperCase()]?.response,
               status: 'success' // Or determine based on status code / response validation
             };
             // Perform frontend validation if needed:
             // callData.frontendValidationStatus = validateData(response.data, callData.schema);
             apiValidationLogStore.getState().updateLog(callData.id, callData); // Update log store
             return response;
          }, error => {
             const startTime = error.config?.meta?.startTime || Date.now();
             const duration = Date.now() - startTime;
             const callData = {
               type: 'response',
               id: error.config?.meta?.callId,
               timestamp: new Date().toISOString(),
               endpoint: error.config?.url,
               method: error.config?.method?.toUpperCase(),
               responseStatus: error.response?.status,
               responseBody: error.response?.data || { error: error.message },
               durationMs: duration,
               // Find relevant schema
               // schema: schemas[error.config.url]?.[error.config.method?.toUpperCase()]?.errorResponse,
               status: 'error'
             };
             apiValidationLogStore.getState().updateLog(callData.id, callData);
             return Promise.reject(error);
          });
        }

        export default apiClient;
        ```

  * **Global Validator Display (`DeveloperToolsPanel.jsx`):**

        ```jsx
        import React from 'react';
        import APIValidator from '../../components/ui_components/APIValidator'; // Adjust path
        import { useApiValidationLogStore } from './stores/apiValidationLogStore'; // Example Zustand hook

        function DeveloperToolsPanel() {
          const apiLogs = useApiValidationLogStore(state => state.logs);

          // Only render in development
          if (process.env.NODE_ENV !== 'development') {
            return null;
          }

          return (
            <div className="dev-tools-panel" style={{ border: '2px solid red', position: 'fixed', bottom: 0, right: 0, maxHeight: '300px', overflowY: 'auto', background: 'lightgray', zIndex: 9999 }}>
              <h3>API Call Log (Dev Mode)</h3>
              {apiLogs.length === 0 && <p>No API calls logged yet.</p>}
              {apiLogs.slice(-10).reverse().map(log => ( // Show last 10, newest first
                 // The APIValidator component now takes structured log data
                 <APIValidator key={log.id} apiCallData={log} />
              ))}
            </div>
          );
        }

        export default DeveloperToolsPanel;

        // Include <DeveloperToolsPanel /> somewhere in your main App layout
        ```

* **Explanation:** This setup uses Axios interceptors (a common pattern) to automatically capture request/response data *only* in development mode. It stores this log data in a global state (e.g., using Zustand or React Context). A dedicated `DeveloperToolsPanel` component subscribes to this store and renders each log entry using the `APIValidator` component, providing a live feed of API interactions for the developer. The `APIValidator` itself focuses purely on displaying the structured `apiCallData` it receives.

---

## 4. Example: Using `DataTraceability` for AI Recommendation Insight

* **Purpose:** To provide users with transparency into *why* a specific recommendation (e.g., a potential match in Mode 2, a suggested community in Mode 3) was made by an AI model.
* **Component Spec:** [`docs/components/ui_components/DataTraceability.md`](../../components/ui_components/DataTraceability.md)
* **Scenario:** A user sees a suggested community ("Ethical Tech Collaborators") in Mode 3 and wants to understand which of their profile values or activities led to this suggestion.

* **Conceptual React Implementation:**

    ```jsx
    import React, { useState } from 'react';
    import DataTraceability from '../../components/ui_components/DataTraceability'; // Adjust path
    import apiClient from './services/apiClient'; // Your API client instance

    function CommunityRecommendation({ recommendation }) {
      const [showTrace, setShowTrace] = useState(false);
      const [traceData, setTraceData] = useState(null);
      const [isLoadingTrace, setIsLoadingTrace] = useState(false);

      const fetchTraceability = async () => {
        if (traceData) { // Toggle if already loaded
          setShowTrace(!showTrace);
          return;
        }
        setIsLoadingTrace(true);
        try {
          // Assume API endpoint provides traceability data for a specific recommendation ID
          const response = await apiClient.get(`/recommendations/community/${recommendation.id}/trace`);
          setTraceData(response.data); // Expects graphData format for the component
          setShowTrace(true);
        } catch (error) {
          console.error("Failed to fetch traceability data:", error);
          alert("Could not load traceability information.");
        } finally {
          setIsLoadingTrace(false);
        }
      };

      return (
        <div className="community-card">
          <h3>{recommendation.name}</h3>
          <p>{recommendation.description}</p>
          <p>Reason: {recommendation.reason || 'Based on your profile'}</p>
          <button onClick={fetchTraceability} disabled={isLoadingTrace}>
            {isLoadingTrace ? 'Loading...' : (showTrace ? 'Hide Details' : 'Why was this recommended?')}
          </button>

          {showTrace && traceData && (
            <div className="traceability-details" style={{ marginTop: '10px', border: '1px solid #ccc', padding: '10px' }}>
              <h4>Data Traceability:</h4>
              <DataTraceability
                  graphData={traceData} // Pass the fetched graph data
                  visualizationConfig={{ /* Optional custom config */ }}
              />
               {/* Link to detailed usage examples */}
               <p><small>See examples: [`docs/guides/examples/DataTraceability_Usage_Examples.md`](../../guides/examples/DataTraceability_Usage_Examples.md)</small></p>
            </div>
          )}
        </div>
      );
    }

    export default CommunityRecommendation;
    ```

* **Explanation:** This component displays a community recommendation. A button allows the user to fetch and view the traceability data *on demand*. When clicked, it calls a hypothetical backend endpoint (`/recommendations/.../trace`) that returns data specifically formatted for the `DataTraceability` component (nodes representing user values/activities, edges representing influence, potentially weighted). The `DataTraceability` component then renders this graph, making the AI's reasoning transparent to the user.

---

These examples illustrate how ThinkAlike's validation-focused UI components can be practically integrated into the development workflow to enforce standards, provide feedback, and enhance transparency, truly embodying the "UI as Validation Framework" principle. Remember to consult the specific component documentation for detailed props and usage.
