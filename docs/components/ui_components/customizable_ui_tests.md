# Design Document: Customizable UI Tests

---

## 1. Introduction and Description

The **Customizable UI Tests** feature embodies ThinkAlike's commitment to **UI as a Validation Framework** and **User Empowerment** in a profound way. It provides an integrated interface within the ThinkAlike platform itself, empowering both developers/testers and potentially authorized users (such as community admins or power users) to **define, configure, execute, and analyze custom testing scenarios directly through the user interface**.

This feature moves beyond traditional, code-centric testing paradigms by:

* **Democratizing Testing:** Making test creation more accessible, even for those less familiar with writing test scripts.
* **Enhancing Transparency:** Allowing users/testers to visually construct and understand test workflows.
* **Facilitating Rapid Validation:** Enabling quick definition and execution of tests for specific features, workflows, or data conditions.
* **Integrating Ethical Checks:** Providing UI elements to incorporate ethical validation assertions directly into test scenarios.
* **Closing the Feedback Loop:** Displaying test results immediately within the same UI environment where tests are defined.

This feature is a key component of the strategy outlined in the [ThinkAlike Testing and Validation Plan](testing_and_validation_plan.md) and relies on underlying concepts from the [UI Testing Framework](UI_Testing_Framework.md) design.

---

## 2. UI Components

This feature typically resides within a dedicated "Testing & Validation Center" or a similar section of the ThinkAlike platform, potentially accessible via developer tools or specific user roles.

### 2.1 Test Template Library

* **Purpose:** To provide users with a collection of predefined test scenarios that can serve as starting points or examples, lowering the barrier for test creation.
* **UI Elements:**
  * **Template Browser:** A searchable and filterable list or grid showcasing available templates. Each template entry includes:
    * Name (e.g., "Login Success Workflow", "Profile Update Validation", "Ethical Bias Check - Mode 2 Matches", "Accessibility Audit - Community Page").
    * Brief Description.
    * Tags/Categories (e.g., 'Authentication', 'UI Validation', 'Ethical', 'Accessibility', 'Mode 2').
  * **Template Preview:** Upon selection, displays the sequence of actions and assertions defined within the template.
  * **"Use Template" / "Clone" Button:** Loads the selected template's steps into the Customizable Testing Scenarios Panel for modification.
* **Data Source:** JSON configurations defining each template, either stored in the frontend codebase or fetched from a backend endpoint (`GET /api/testing/templates`).

### 2.2 Customizable Testing Scenarios Panel ("Scenario Builder")

* **Purpose:** The core interactive workspace for visually constructing, configuring, saving, and loading custom test scenarios.
* **UI Elements:**
  * **Scenario Metadata:** Input fields for `Scenario Name` and `Scenario Description`.
  * **Step Sequencer:** Primary area where users build the test flow. Options include:
    * *Drag-and-Drop Interface:* Users drag predefined Action Blocks and Assertion Blocks from a palette into the sequence.
    * *Step-by-Step Wizard:* A guided process where users add steps sequentially.
  * **Action Blocks Palette:** A list of available actions representing user interactions or system events:
    * `Navigate To [URL]`
    * `Click Element [Selector]`
    * `Enter Text [Selector, Text Value]`
    * `Select Option [Selector, Value/Label]`
    * `Wait For Element [Selector, Timeout]`
    * `Wait [Milliseconds]`
    * `Call API [Endpoint, Method, Payload]` (Requires careful security considerations)
    * `Set Mock Data [Context, Data]` (For injecting test data)
  * **Assertion Blocks Palette:** A list of available validation checks:
    * `Expect Element Exists [Selector]`
    * `Expect Element Visible [Selector]`
    * `Expect Text Equals [Selector, Expected Text]`
    * `Expect Value Equals [Selector, Expected Value]` (For input fields)
    * `Expect API Response Status [Expected Status Code]`
    * `Expect API Response Contains [JSON Path, Expected Value]`
    * `Expect Data Point Validates [Data Point Ref, Validation Rule]`
    * `Expect Ethical Score Above [Threshold, Context Ref]` (Integrates with `CoreValuesValidator` logic)
    * `Expect No Accessibility Violations [WCAG Level, Scope Selector]`
    * `Expect Performance Metric Below [Metric Name, Threshold]` (e.g., 'RenderTime', 'APIDuration')
  * **Parameter Configuration:** When an Action or Assertion block is added to the sequence, a configuration panel appears that allows users to input necessary parameters (CSS selectors, URLs, text values, expected results, thresholds). This integrates with Data Validation Parameters (see below).
  * **Control Buttons:** `Run Test`, `Save Scenario`, `Load Scenario`, `Clear Scenario`.
* **Data Source:** User interactions within the builder. Saved scenarios are stored locally (e.g., in localStorage) or on the backend (`POST /api/testing/scenarios`).

### 2.3 Data Validation Parameters (Integrated UI Helpers)

* **Purpose:** To simplify the configuration of test parameters by leveraging the live UI and existing data components.
* **UI Elements:**
  * **Element Selector Tool:** A mode (activated via a button in the Scenario Builder) that lets the user click directly on elements in the main ThinkAlike UI (rendered alongside or in an iframe) to capture their CSS selectors for use in Action/Assertion blocks.
  * **Data Point Picker:** Integration with the Data Explorer Panel or similar views, allowing users to select specific data points (e.g., a user profile field, an AI recommendation attribute) for use in assertions.
  * **Contextual Parameter Suggestions:** Based on the selected Action/Assertion block, the UI may suggest relevant parameters or selectors based on the current application state or common patterns.

### 2.4 Data Visualization Tools (Test Results Display)

* **Purpose:** To present the outcomes of test runs clearly, actionably, and comprehensively.
* **UI Elements (Often in a separate Test Results view/panel):**
  * **Run History:** A list of previous test runs with timestamps, scenario names, and overall pass/fail status.
  * **Detailed Report:** For each selected run, display:
    * *Overall Summary:* Pass/Fail status, run duration, number of steps/assertions.
    * *Step-by-Step Results:* Each executed step shows:
      * The action or assertion performed.
      * Status (Pass, Fail, or Skipped).
      * Duration.
      * Screenshots, logs, or error messages (especially for failures).
      * Visual diff comparison (if visual regression tests are implemented).
    * *Aggregated Reports:* Sections summarizing results for specific categories such as:
      * Performance Metrics (charts visualizing load times, API durations).
      * Ethical Compliance Report (summary from CoreValuesValidator assertions).
      * Accessibility Report (list of violations found).
* **Data Source:** Data generated by the test execution engine during each run, stored temporarily or fetched from (`GET /api/testing/results/:runId`).

---

## 3. Actionable Parameters (Defining Tests via UI)

* **Data Testing via UI:** Users define test data directly in action blocks (for example, `Enter Text`) or use mock data injection. Assertions (such as `Expect Text Equals` or `Expect Data Point Validates`) then verify the system's handling of this UI-defined data.
* **Code Validation via UI:** Tests defined in the UI validate behavior resulting from code execution:
  * UI state changes are validated (e.g., `Expect Element Visible`, `Expect Text Equals`).
  * Frontend logic triggering API calls is validated by asserting on subsequent UI changes or by inspecting the API call itself (`Call API`, `Expect API Response Status`).
  * Backend code is implicitly validated by asserting on the API responses and the resulting data/UI state changes.
  * Ethical code implementation is validated using specific ethical assertions (`Expect Ethical Score Above`), which rely on CoreValuesValidator logic (potentially involving backend verification calls).

---

## 4. Code Implementation Notes

* **Framework:** React.
* **Core Challenge: Test Execution Engine:** How to translate UI-defined steps into actual browser actions and assertions:
  * **Frontend Engine:** Use testing-library or custom simulation to simulate clicks, typing, and element state checks within the React component tree (good for component-level tests, but limited for true end-to-end (E2E) testing).
  * **Browser Automation Integration (Recommended for E2E):** The UI acts as a script generator – the Scenario Builder creates a test script (in Cypress, Playwright, or Selenium format). A separate process (triggered via a backend API call or integrated local test runner) then executes this script against a running instance of the application.
  * **Backend Orchestration:** The UI sends the scenario definition (in JSON format) to a backend testing service (e.g., via `POST /api/testing/run`). The backend then uses Selenium Grid, Playwright Service, or a similar tool to spin up browser instances, execute the steps, and report results back. This approach is scalable and robust but requires additional backend infrastructure.
* **Scenario Definition Format:** Define a clear JSON schema for representing test scenarios (including steps, actions, assertions, and parameters).
* **Component Communication:** Use appropriate state management for the Scenario Builder and for displaying test results.
* **Security:** Critical if users can define tests:
  * Sanitize all user inputs (selectors, text values, URLs).
  * Restrict certain actions and assertions based on user roles – for example, non-developers should have limited access to actions like `Call API` or arbitrary script execution.
  * If using a backend execution engine, run tests in isolated environments (e.g., Docker containers) and validate API calls triggered by tests against user permissions.
* **Modularity:** Design Action Blocks and Assertion Blocks as pluggable modules so that the framework can be extended easily.

---

## 5. Testing Instructions (Testing the Test Feature Itself)

* **Scenario Builder:**
  * Verify drag-and-drop or step-by-step sequencing works correctly.
  * Test adding, removing, and reordering steps.
  * Test the configuration panel for each Action/Assertion block – ensure parameters are saved and loaded correctly.
  * Test the Element Selector Tool integration – verify it accurately captures CSS selectors.
  * Test the Save/Load Scenario functionality.
* **Test Execution:**
  * Create simple scenarios (e.g., navigate to a URL and check heading text) and run them. Confirm correct execution and a pass status.
  * Create scenarios designed to fail (e.g., expect a non-existent element or incorrect text) and verify proper failure status and error reporting.
  * Test scenarios that involve various Action/Assertion types (including API calls, ethical checks, and accessibility checks).
  * Validate handling of timeouts and errors during test execution.
* **Results Display:**
  * Confirm that the dashboard and detailed reports accurately reflect the outcomes of test runs.
  * Ensure that logs, screenshots (if implemented), performance charts, and ethical/accessibility reports display correctly.
* **Security:**
  * Try injecting malicious scripts or selectors via parameter inputs. Verify that sanitization prevents XSS or unintended actions.
  * Test that role-based access to the feature works as expected.

---

## 6. UI Mockup Placeholder

Refer to the project's central design repository for visual mockups.
[Placeholder: Link or embed visual mockups of the Customizable UI Tests feature, including the Scenario Builder and Test Results Dashboard/Report view.]

---

## 7. Dependencies & Integration

* **Depends On:**
  * Core reusable UI components (Buttons, Inputs, Modals, Lists).
  * Potentially the Data Explorer Panel (for data point selection).
  * CoreValuesValidator (for ethical assertions).
  * Accessibility audit libraries (e.g., axe-core).
  * Backend Testing Service/API (if using backend or hybrid execution).
  * Browser automation frameworks (Cypress, Playwright, Selenium – depending on the chosen execution engine).
  * [ThinkAlike Style Guide](../../guides/developer_guides/style_guide.md).
* **Integrates With:**
  * The overall platform's authentication/authorization to control access.
  * The Developer Tools panel or a dedicated Testing section.
  * The CI/CD pipeline (potentially triggering saved UI tests via an API).

---

## 8. Future Enhancements

* Visual regression testing (comparing screenshots).
* Support for conditional logic within test scenarios (if/else).
* Creation of reusable "functions" or sub-scenarios.
* Parameterizing scenarios to run with different data sets.
* Integration with code coverage reporting.
* Support for testing mobile views or different browser types.
* AI-assisted test generation based on user flows or requirements.

---
