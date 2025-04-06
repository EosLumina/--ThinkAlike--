# Customizable Ui Tests

---

## 1. Introduction and Description

The **Customizable UI Tests** feature embodies ThinkAlike's commitment to **UI as a Validation Framework** and **User Empowerment** in a profound way. It provides an integrated interface *within* the ThinkAlike platform itself, empowering both developers/testers and potentially authorized users (like community admins or power users in specific contexts) to **define, configure, execute, and analyze custom testing scenarios directly through the user interface**.

This feature moves beyond traditional, code-centric testing paradigms by:

*   **Democratizing Testing:** Making test creation more accessible, even for those less familiar with coding test scripts.
*   **Enhancing Transparency:** Allowing users/testers to visually construct and understand test workflows.
*   **Facilitating Rapid Validation:** Enabling quick definition and execution of tests for specific features, workflows, or data conditions.
*   **Integrating Ethical Checks:** Providing UI elements to incorporate ethical validation assertions directly into test scenarios.
*   **Closing the Feedback Loop:** Displaying test results immediately within the same UI environment where tests are defined.

This feature is a key component of the strategy outlined in the [ThinkAlike Testing and Validation Plan](testing_and_validation_plan.md) and relies on underlying concepts from the [UI Testing Framework](UI_Testing_Framework.md) design.

---

## 2. UI Components

This feature typically resides within a dedicated "Testing & Validation Center" or a similar privileged section of the ThinkAlike platform, potentially accessible via developer tools or specific user roles.

### 2.1 Test Template Library

*   **Purpose:** To provide users with a collection of pre-defined, common test scenarios that can be used as starting points or examples. This lowers the barrier to entry for creating tests.
*   **UI Elements:**
    *   **Template Browser:** A searchable and filterable list/grid view showcasing available templates. Each template entry includes:
        *   Name (e.g., "Login Success Workflow", "Profile Update Validation", "Ethical Bias Check - Mode 2 Matches", "Accessibility Audit - Community Page").
        *   Brief Description.
        *   Tags/Categories (e.g., 'Authentication', 'UI Validation', 'Ethical', 'Accessibility', 'Mode 2').
    *   **Template Preview:** On selection, displays the sequence of actions and assertions defined within the template.
    *   **"Use Template" / "Clone" Button:** Loads the selected template's steps into the Customizable Testing Scenarios Panel for modification.
*   **Data Source:** JSON configurations defining each template, potentially stored in the frontend codebase or fetched from a backend endpoint (`GET /api/testing/templates`).

### 2.2 Customizable Testing Scenarios Panel ("Scenario Builder")

*   **Purpose:** The core interactive workspace for visually constructing, configuring, saving, and loading custom test scenarios.
*   **UI Elements:**
    *   **Scenario Metadata:** Input fields for `Scenario Name` and `Scenario Description`.
    *   **Step Sequencer:** A primary area where users build the test flow. This could be:
        *   *Drag-and-Drop Interface:* Users drag predefined "Action Blocks" and "Assertion Blocks" from a palette into the sequence.
        *   *Step-by-Step Wizard:* A guided process where users add steps sequentially.
    *   **Action Blocks Palette:** A list of available actions representing user interactions or system events:
        *   `Navigate To [URL]`
        *   `Click Element [Selector]`
        *   `Enter Text [Selector, Text Value]`
        *   `Select Option [Selector, Value/Label]`
        *   `Wait For Element [Selector, Timeout]`
        *   `Wait [Milliseconds]`
        *   `Call API [Endpoint, Method, Payload]` (Requires careful security considerations)
        *   `Set Mock Data [Context, Data]` (For injecting test data)
    *   **Assertion Blocks Palette:** A list of available validation checks:
        *   `Expect Element Exists [Selector]`
        *   `Expect Element Visible [Selector]`
        *   `Expect Text Equals [Selector, Expected Text]`
        *   `Expect Value Equals [Selector, Expected Value]` (For input fields)
        *   `Expect API Response Status [Expected Status Code]`
        *   `Expect API Response Contains [JSON Path, Expected Value]`
        *   `Expect Data Point Validates [Data Point Ref, Validation Rule]`
        *   `Expect Ethical Score Above [Threshold, Context Ref]` (Integrates with `CoreValuesValidator` logic)
        *   `Expect No Accessibility Violations [WCAG Level, Scope Selector]`
        *   `Expect Performance Metric Below [Metric Name, Threshold]` (e.g., 'RenderTime', 'APIDuration')
    *   **Parameter Configuration:** When an Action/Assertion block is added to the sequence, a configuration panel appears allowing users to input necessary parameters (CSS Selectors, URLs, text values, expected results, thresholds). Integration with "Data Validation Parameters" (see below) aids this.
    *   **Control Buttons:** `Run Test`, `Save Scenario`, `Load Scenario`, `Clear Scenario`.
*   **Data Source:** User interactions within the builder. Saved scenarios stored locally (localStorage) or on the backend (`POST /api/testing/scenarios`).

### 2.3 Data Validation Parameters (Integrated UI Helpers)

*   **Purpose:** To simplify the configuration of test parameters by leveraging the live UI and existing data components.
*   **UI Elements:**
    *   **Element Selector Tool:** A mode (e.g., activated by a button in the Scenario Builder) that allows the user to click directly on elements in the main ThinkAlike UI (rendered alongside or in a frame) to automatically capture their CSS selectors for use in Action/Assertion blocks.
    *   **Data Point Picker:** Integration with the `Data Explorer Panel` or similar data views, allowing users to select specific data points (e.g., a user profile field, an AI recommendation attribute) to use in assertion blocks.
    *   **Contextual Parameter Suggestions:** Based on the selected Action/Assertion block, the UI might suggest relevant parameters or selectors based on the current application state or common patterns.

### 2.4 Data Visualization Tools (Test Results Display)

*   **Purpose:** To present the outcomes of test runs in a clear, actionable, and comprehensive manner.
*   **UI Elements (Often in a separate "Test Results" view/panel):**
    *   **Run History:** A list of previous test runs with timestamps, scenario names, and overall pass/fail status.
    *   **Detailed Report:** For a selected run:
        *   *Overall Summary:* Pass/Fail status, duration, number of steps/assertions.
        *   *Step-by-Step Results:* A list of executed steps, each showing:
            *   Action/Assertion performed.
            *   Status (Pass/Fail/Skipped).
            *   Duration.
            *   Screenshots/Logs/Error messages (especially for failures).
            *   Visual diff comparison (for visual regression tests, if implemented).
        *   *Aggregated Reports:* Dedicated sections summarizing results for specific categories:
            *   Performance Metrics (Charts visualizing load times, API durations).
            *   Ethical Compliance Report (Summary from `CoreValuesValidator` assertions).
            *   Accessibility Report (List of violations found).
*   **Data Source:** Data generated by the test execution engine during a run, passed to the UI for rendering. Potentially stored temporarily or fetched from (`GET /api/testing/results/:runId`).

---

## 3. Actionable Parameters (Defining Tests via UI)

*   **Data Testing via UI:** Users define test data directly in action blocks (e.g., `Enter Text`) or use mock data injection steps. Assertions (`Expect Text Equals`, `Expect Data Point Validates`) then check the system's handling of this UI-defined data.
*   **Code Validation via UI:** Tests defined in the UI validate the *behavior* resulting from code execution.
    *   UI state changes are validated (`Expect Element Visible`, `Expect Text Equals`).
    *   Frontend logic triggering API calls is validated by asserting on subsequent UI changes or mocking/inspecting the API call itself (`Call API`, `Expect API Response Status`).
    *   Backend code is implicitly validated by asserting on the API responses and the resulting data/UI state changes.
    *   Ethical code implementation is validated using specific ethical assertions (`Expect Ethical Score Above`) which rely on the `CoreValuesValidator` logic (potentially involving backend Verification System calls).

---

## 4. Code Implementation Notes

*   **Framework:** React.
*   **Core Challenge: Test Execution Engine:** How are the UI-defined steps translated into actual browser actions and assertions?
    *   **Frontend Engine (e.g., using `testing-library` or custom simulation):** The UI itself simulates clicks, typing, checks element states within the React component tree. Good for component-level tests, limited for true E2E or complex navigation/API interaction.
    *   **Browser Automation Integration (Recommended for E2E):** The UI acts as a "script generator." The Scenario Builder creates a test script (e.g., in Cypress, Playwright, or Selenium format/commands). A separate process (potentially triggered via a backend API call or a local test runner integrated with developer tools) executes this script against a running instance of the application (local or staging).
    *   **Backend Orchestration:** The UI sends the scenario definition (`JSON`) to a backend testing service (`POST /api/testing/run`). The backend uses Selenium Grid, Playwright Service, or similar to spin up browser instances, execute the steps, and report results back. This is the most scalable and robust approach but requires significant backend infrastructure.
*   **Scenario Definition Format:** Define a clear JSON schema for representing the test scenarios (steps, actions, assertions, parameters).
*   **Component Communication:** Use state management for the Scenario Builder state and for displaying results.
*   **Security:** Critically important if users can define tests.
    *   Sanitize *all* user inputs used as parameters (selectors, text values, URLs).
    *   Restrict available actions/assertions based on user roles. Non-developers should likely not have access to `Call API` or arbitrary script execution steps.
    *   If using a backend execution engine, run tests in isolated environments (e.g., Docker containers). Validate API calls triggered by tests against user permissions.
*   **Modularity:** Design Action Blocks and Assertion Blocks as pluggable modules to easily extend the framework's capabilities.

---

## 5. Testing Instructions (Testing the Test Feature Itself)

*   **Scenario Builder:**
    *   Verify drag-and-drop / step-by-step sequencing works correctly.
    *   Test adding, removing, and reordering steps.
    *   Test configuration panel for each Action/Assertion block – ensure parameters are saved and loaded correctly.
    *   Test Element Selector Tool integration – verify it accurately captures selectors.
    *   Test Save/Load Scenario functionality.
*   **Test Execution:**
    *   Create simple scenarios (e.g., navigate, check heading text) and run them. Verify correct execution and pass status.
    *   Create scenarios designed to fail (e.g., expect non-existent element, expect wrong text). Verify correct failure status and error reporting.
    *   Test scenarios involving various Action/Assertion types (API calls, ethical checks, accessibility checks).
    *   Test handling of timeouts and errors during test execution.
*   **Results Display:**
    *   Verify the dashboard and detailed reports accurately reflect the outcome of test runs.
    *   Ensure logs, screenshots (if implemented), performance charts, and ethical/accessibility reports display correctly.
*   **Security:** Attempt to inject malicious scripts or selectors via parameter inputs. Verify sanitization prevents XSS or unintended actions. Test role-based access to the feature.

---

## 6. UI Mockup Placeholder

*Refer to the project's central design repository for visual mockups.*

`[Placeholder: Link or embed visual mockups of the Customizable UI Tests feature, including the Scenario Builder interface and the Test Results Dashboard/Report view, here]`

---

## 7. Dependencies & Integration

*   **Depends On:**
    *   Core reusable UI components (Buttons, Inputs, Modals, Lists).
    *   Potentially `Data Explorer Panel` (for data point selection).
    *   `CoreValuesValidator` (for ethical assertions).
    *   Accessibility audit libraries (`axe-core`).
    *   Backend Testing Service/API (if using backend/hybrid execution).
    *   Browser automation framework (Cypress, Playwright, Selenium - depending on execution engine).
    *   [ThinkAlike Style Guide](../../guides/developer_guides/style_guide.md).
*   **Integrates With:**
    *   Overall platform authentication/authorization (to control access).
    *   Developer Tools panel or dedicated Testing section.
    *   CI/CD pipeline (potentially triggering saved UI tests via API).

---

## 8. Future Enhancements

*   Visual regression testing (comparing screenshots).
*   Support for conditional logic within test scenarios (if/else).
*   Creating reusable "functions" or sub-scenarios.
*   Parameterizing scenarios to run with different data sets.
*   Integration with code coverage reporting.
*   Support for testing mobile views or different browser types.
*   AI-assisted test generation based on user flows or requirements.

---
