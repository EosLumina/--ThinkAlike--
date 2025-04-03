# ThinkAlike: Standard Test Report Schema Specification

**Version:** 1.0
**Date:** March 26, 2025

---

## 1. Introduction

This document specifies the **standard JSON schema** for comprehensive **Test Reports** generated within the ThinkAlike project. This schema provides a standardized format for aggregating the results of multiple individual test cases executed as part of a specific test run or suite.

Using this standardized report structure facilitates:

*   **Consistent Reporting:** Ensures uniformity across different testing types (Unit, Integration, E2E, Performance, Security, Ethical, UAT).
*   **Automated Analysis:** Allows tools and dashboards to easily parse and analyze test outcomes, track trends, and calculate metrics.
*   **Clear Visualization:** Provides a predictable structure for UI components (like those in the `Customizable UI Tests` feature or CI/CD dashboards) to display test results effectively.
*   **Integration:** Simplifies integration with CI/CD pipelines and project management tools.

This schema often incorporates individual test results structured according to the [Standard Data Output Schema](./data_output_schema.md).

---

## 2. Schema Definition (`test_report.json` Structure)

The following describes the structure for a Test Report object, typically representing the output of a single execution of a test suite or test plan.

```json
{
  "reportId": {
    "type": "string",
    "description": "Unique identifier for this specific test report instance (e.g., UUID, CI build number, timestamp-based ID).",
    "required": true,
    "example": "testrun_a1b2c3d4_20250326T150000Z"
  },
  "generationTimestamp": {
    "type": "string",
    "format": "date-time",
    "description": "ISO 8601 timestamp: When this JSON report was generated.",
    "required": true,
    "example": "2025-03-26T15:05:00Z"
  },
  "testExecution": {
    "type": "object",
    "description": "Metadata about the test execution itself.",
    "properties": {
      "startTimestamp": {
        "type": "string",
        "format": "date-time",
        "description": "ISO 8601 timestamp: When the test execution began.",
        "required": true,
        "example": "2025-03-26T15:00:00Z"
      },
      "endTimestamp": {
        "type": "string",
        "format": "date-time",
        "description": "ISO 8601 timestamp: When the test execution completed.",
        "required": true,
        "example": "2025-03-26T15:04:30Z"
      },
      "durationMs": {
        "type": "number",
        "description": "Total duration of the test execution in milliseconds.",
        "required": true,
        "example": 270000
      },
      "triggeredBy": {
        "type": "string",
        "description": "Identifier of the entity that triggered the test run (e.g., 'CI Pipeline', 'User: john_doe', 'Scheduled Task').",
        "required": false
      }
    },
    "required": ["startTimestamp", "endTimestamp", "durationMs"]
  },
  "testEnvironment": {
    "type": "object",
    "description": "Details about the environment where the tests were executed.",
    "properties": {
      "platform": { "type": "string", "enum": ["local", "ci", "staging", "production", "custom"], "description": "The general environment type." },
      "os": { "type": "string", "description": "OS details (e.g., 'Ubuntu 22.04', 'Windows 11', 'macOS Sonoma')." },
      "browser": { "type": "string", "description": "Browser details for UI tests (e.g., 'Chrome 123.0', 'Firefox 122')." },
      "backendVersion": { "type": "string", "description": "Version identifier (e.g., Git commit hash, tag) of the backend code tested." },
      "frontendVersion": { "type": "string", "description": "Version identifier (e.g., Git commit hash, tag) of the frontend code tested." },
      "databaseVersion": { "type": "string", "description": "Version of the database schema or database server, if relevant." },
      "nodeVersion": { "type": "string", "description": "Node.js version used for frontend tests/build." },
      "pythonVersion": { "type": "string", "description": "Python version used for backend tests." }
      // Other relevant details like hardware specs if performance testing
    },
    "required": false
  },
  "testSuite": {
    "type": "object",
    "description": "Information about the test suite or collection of tests covered by this report.",
    "properties": {
      "name": { "type": "string", "description": "Human-readable name of the test suite (e.g., 'API Endpoint Security Checks', 'Mode 1 Narrative Flow Validation').", "required": true },
      "type": {
        "type": "string",
        "enum": ["unit", "integration", "ui_e2e", "ui_component", "performance", "security", "ethical", "uat", "regression", "smoke", "custom"],
        "description": "The primary testing methodology or category.",
        "required": true
      },
      "description": { "type": "string", "description": "Optional brief description of the suite's goals." }
    },
    "required": ["name", "type"]
  },
  "summary": {
    "type": "object",
    "description": "Aggregated summary statistics for the entire test run.",
    "properties": {
      "overallStatus": {
        "type": "string",
        "enum": ["pass", "fail", "warning", "error", "skipped"],
        "description": "The overall consolidated outcome (e.g., 'fail' if any test case failed)."
      },
      "totalTests": { "type": "integer", "minimum": 0, "description": "Total number of individual test cases executed." },
      "passed": { "type": "integer", "minimum": 0, "description": "Number of test cases with status 'pass'." },
      "failed": { "type": "integer", "minimum": 0, "description": "Number of test cases with status 'fail' or 'error'." },
      "warnings": { "type": "integer", "minimum": 0, "description": "Number of test cases with status 'warning'." },
      "skipped": { "type": "integer", "minimum": 0, "description": "Number of test cases with status 'skipped'." },
      // Add other summary metrics like average duration, key ethical scores, etc. if applicable
      "coverage": {
          "type": "object",
          "description": "Optional code coverage summary.",
          "properties": {
              "lines": { "type": "number", "format": "float", "minimum": 0, "maximum": 100 },
              "branches": { "type": "number", "format": "float", "minimum": 0, "maximum": 100 },
              "functions": { "type": "number", "format": "float", "minimum": 0, "maximum": 100 }
          },
          "required": false
      }
    },
    "required": ["overallStatus", "totalTests", "passed", "failed", "warnings", "skipped"]
  },
  "results": {
    "type": "array",
    "description": "An array containing detailed results for each individual test case within the suite.",
    "items": {
      // Schema for an individual test case result
      "type": "object",
      "properties": {
        "testCaseId": { "type": "string", "description": "Unique name or ID for this test case (e.g., 'test_user_login_success', 'validate_profile_update_api').", "required": true },
        "description": { "type": "string", "description": "Human-readable description of the test case objective." },
        "status": {
          "type": "string",
          "enum": ["pass", "fail", "warning", "skipped", "error"], // Added 'error' for test setup failures
          "description": "Outcome of this specific test case.",
          "required": true
        },
        "durationMs": { "type": "number", "description": "Execution time for this test case in milliseconds." },
        "steps": { // Optional structured steps
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "description": "Action performed (e.g., 'Click button', 'Assert text')."},
                    "status": {"type": "string", "enum": ["pass", "fail"]},
                    "details": {"type": "string", "description": "Observation or result."}
                }
            }
        },
        "error": { // Details if status is 'fail' or 'error'
          "type": "object",
          "properties": {
            "message": { "type": "string", "description": "The primary error message or assertion failure." },
            "type": { "type": "string", "description": "Type of error (e.g., 'AssertionError', 'TimeoutError', 'APIError')." },
            "stackTrace": { "type": "string", "description": "Full stack trace, if available." }
          }
        },
        "outputData": { // Standardized output related to the test
            "type": "array",
            "items": { "$ref": "data_output_schema.md#/" }, // Array of standard data outputs
            "description": "Optional array of structured outputs generated during the test (e.g., performance metrics, validation results) following the standard data output schema."
        },
        "tags": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Optional tags for categorizing the test case (e.g., 'smoke', 'regression', 'mode-2', 'security')."
        },
        "logs": { // Captured logs for this specific test
             "type": "array",
             "items": { "type": "string" }
        },
        "screenshotUrl": { // Link to screenshot on failure
            "type": "string",
            "format": "url"
        }
        // Add other test-case specific fields as needed
      },
      "required": ["testCaseId", "status"]
    },
    "required": true
  }
}
```

---

## 3. Key Fields Explained

*   **Report Metadata:** `reportId`, `generationTimestamp`, `testExecution` block provide context about the report itself and when the tests ran.
*   **testEnvironment:** Crucial for diagnosing environment-specific failures.
*   **testSuite:** Identifies the scope and type of tests covered.
*   **summary:** Provides the essential pass/fail statistics at a glance. Includes optional code coverage.
*   **results:** The core array holding details for each test case.
  *   `testCaseId`, `description`, `status`, `durationMs`: Basic info for each test.
  *   `steps`: Optional breakdown for complex tests.
  *   `error`: Detailed failure information.
  *   `outputData`: Crucially links to the data_output_schema for standardized, detailed results (like specific validation failures, performance numbers, ethical scores generated during the test).
  *   `tags`: Useful for filtering and organizing results.
  *   `logs`, `screenshotUrl`: Aid debugging.

---

## 4. Usage

*   **Test Runners:** Configure test frameworks (pytest, Jest, Cypress, etc.) to output results in this JSON format (may require custom reporters or adapters).
*   **CI/CD Pipelines:** Parse these reports to determine build status, display summaries, track metrics over time, and potentially gate deployments.
*   **Testing Dashboards:** UI dashboards (like the one for Customizable UI Tests or external tools like ReportPortal) can consume this format to provide interactive visualization of test results.
*   **Analysis:** The structured format allows for automated analysis of failure patterns, test flakiness, performance regressions, or ethical compliance trends.

---

## 5. Implementation Notes

*   **Consistency:** While `value` is flexible, strive for consistent structures within the same `dataType`. For example, all outputs with `dataType`: "performance_metric" should likely have a `value` object with `metric`, `value`, and `unit` fields.
*   **Granularity:** Decide on the appropriate level of granularity for outputs. Should one user action generate one output, or multiple outputs for different aspects (performance, validation, ethical)? This depends on the consuming system.
*   **Context is Key:** Ensure `sourceComponent` and `workflowContext` provide enough context to understand where the output originated.
*   **UI Integration:** Design UI components (DataDisplay, dashboards) to intelligently render different parts of this schema based on the `dataType` and the presence of optional fields like `validation` or `ethicalCompliance`.

---

## 6. Schema Location

This schema definition resides in `docs/templates/test_report_schema.md`.

Example JSON instances conforming to this schema could be placed in `docs/templates/examples/` or generated by actual test runs.

This standardized schema provides a robust foundation for reporting and analyzing test results across the diverse testing needs of the ThinkAlike project.
