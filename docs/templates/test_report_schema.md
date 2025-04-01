# ThinkAlike: Standard Test Report Schema Specification

---

## 1. Introduction

This document specifies the **standard JSON schema** for comprehensive test reports generated within the ThinkAlike project. This schema standardizes the output format for various testing methodologies (Unit, Integration, UI, Performance, Security, Ethical, UAT), facilitating consistent reporting, automated analysis, and clear visualization in testing dashboards or UI components.

Using a standardized report schema ensures that results from different test suites and tools can be aggregated, compared, and analyzed effectively, providing a holistic view of platform quality, reliability, and ethical compliance. It forms a key part of the data flow within the [Testing and Validation Plan](../../guides/developer_guides/testing_and_validation_plan.md).

---

## 2. Schema Definition (`test_report.json` Structure)

The following outlines the structure and fields intended for a standard `test_report.json` object, representing the results of a single test run or suite execution.

```json
{
  "reportId": {
    "type": "string",
    "description": "Unique identifier for this specific test report (e.g., UUID, build number + timestamp).",
    "required": true
  },
  "generationTimestamp": {
    "type": "string",
    "format": "date-time",
    "description": "ISO 8601 timestamp indicating when this report was generated.",
    "required": true
  },
  "testExecutionTimestamp": {
    "type": "string",
    "format": "date-time",
    "description": "ISO 8601 timestamp indicating when the test execution started.",
    "required": true
  },
  "testExecutionDurationMs": {
    "type": "number",
    "description": "Total duration of the test execution in milliseconds.",
    "required": true
  },
  "testEnvironment": {
    "type": "object",
    "description": "Details about the environment where the tests were run.",
    "properties": {
      "platform": { "type": "string", "description": "e.g., 'local', 'staging', 'production', 'CI'." },
      "os": { "type": "string", "description": "Operating system details, if relevant." },
      "browser": { "type": "string", "description": "Browser name and version, if relevant (for UI tests)." },
      "backendVersion": { "type": "string", "description": "Version/commit hash of the backend code tested." },
      "frontendVersion": { "type": "string", "description": "Version/commit hash of the frontend code tested." }
      // Add other relevant environment details
    },
    "required": false
  },
  "testSuite": {
    "type": "object",
    "description": "Information about the test suite or specific test context.",
    "properties": {
      "name": { "type": "string", "description": "Name of the test suite (e.g., 'API Authentication Tests', 'Mode 2 Matching Algorithm Validation')." },
      "type": {
        "type": "string",
        "enum": ["unit", "integration", "ui_e2e", "ui_component", "performance", "security", "ethical", "uat", "custom"],
        "description": "The primary type of testing methodology employed."
      },
      "description": { "type": "string", "description": "Optional description of the test suite's purpose." }
    },
    "required": true
  },
  "summary": {
    "type": "object",
    "description": "High-level summary of the test results.",
    "properties": {
      "overallStatus": {
        "type": "string",
        "enum": ["pass", "fail", "warning", "error", "skipped"],
        "description": "The overall outcome of the test suite execution."
      },
      "totalTests": { "type": "integer", "description": "Total number of individual test cases executed." },
      "passed": { "type": "integer", "description": "Number of passed test cases." },
      "failed": { "type": "integer", "description": "Number of failed test cases." },
      "warnings": { "type": "integer", "description": "Number of tests completed with warnings (e.g., ethical threshold borderline)." },
      "skipped": { "type": "integer", "description": "Number of skipped test cases." }
    },
    "required": true
  },
  "results": {
    "type": "array",
    "description": "Detailed results for each individual test case executed.",
    "items": {
      "type": "object",
      "properties": {
        "testCaseId": { "type": "string", "description": "Unique identifier or name for the individual test case." },
        "description": { "type": "string", "description": "Description of what the test case verifies." },
        "status": {
          "type": "string",
          "enum": ["pass", "fail", "warning", "skipped"],
          "description": "Outcome of this specific test case."
        },
        "durationMs": { "type": "number", "description": "Duration of this test case in milliseconds." },
        "steps": {
          "type": "array",
          "description": "Optional sequence of steps performed within the test case.",
          "items": {
            "type": "object",
            "properties": {
              "stepDescription": { "type": "string" },
              "status": { "type": "string", "enum": ["pass", "fail"] },
              "details": { "type": "string", "description": "Details or observations for the step." }
            }
          }
        },
        "parameters": {
          "type": "object",
          "description": "Input parameters or configuration used for this test case.",
          "additionalProperties": true
        },
        "output": {
          "allOf": [ { "$ref": "data_output_schema.md#/" } ],
          "description": "The structured data output generated by the test case execution, conforming to the standard Data Output Schema. Optional.",
          "required": false
        },
        "error": {
          "type": "object",
          "description": "Details of the error if the test case failed.",
          "properties": {
            "message": { "type": "string" },
            "stackTrace": { "type": "string" },
            "type": { "type": "string", "description": "e.g., 'AssertionError', 'APIError', 'EthicalViolation', 'AccessibilityViolation'." }
          },
          "required": false
        },
        "logs": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Relevant log messages captured during the test case execution.",
          "required": false
        },
        "screenshots": {
          "type": "array",
          "items": { "type": "string", "format": "url" },
          "description": "Links to screenshots captured during the test (especially on failure).",
          "required": false
        },
        "ethicalComplianceResult": {
          "$ref": "data_output_schema.md#/properties/ethicalCompliance",
          "description": "Specific ethical compliance assessment for this test case. Optional.",
          "required": false
        },
        "accessibilityViolations": {
          "type": "array",
          "items": { "type": "object" },
          "description": "List of accessibility violations detected. Optional.",
          "required": false
        },
        "performanceMetrics": {
          "type": "object",
          "description": "Specific performance metrics captured for this test case.",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "value": { "type": "number" },
              "unit": { "type": "string" }
            }
          },
          "required": false
        }
      },
      "required": ["testCaseId", "status"]
    },
    "required": true
  },
  "recommendations": {
    "type": "array",
    "items": { "type": "string" },
    "description": "Optional list of actionable recommendations based on the overall test results (e.g., 'Investigate API performance under load', 'Review bias metrics for Matching Algorithm').",
    "required": false
  }
}
```

---

## 3. Key Fields Explained

- **reportId, generationTimestamp, testExecutionTimestamp, testExecutionDurationMs:** Provide essential metadata about the report and the test run timing.
- **testEnvironment:** Crucial for reproducibility and understanding context (e.g., failures only occurring in a specific browser or environment).
- **testSuite:** Identifies the set of tests being reported (name and type).
- **summary:** Gives a quick, high-level overview of the pass/fail status.
- **results:** The core array containing details for each individual test case.
  - **testCaseId, description:** Identify the specific test.
  - **status:** The outcome of the test case.
  - **steps:** Allows breaking down complex tests into smaller, verifiable actions.
  - **parameters:** Records the inputs used, aiding in debugging.
  - **output:** Links to the data_output_schema for standardized output capture.
  - **error:** Detailed information if the test failed.
  - **logs, screenshots:** Provide debugging context.
  - **ethicalComplianceResult, accessibilityViolations, performanceMetrics:** Allow specific types of validation results to be clearly reported within the context of the test case.
- **recommendations:** Provides actionable next steps based on the report findings.

---

## 4. Usage

Automated testing frameworks (backend: pytest, frontend: Jest/Vitest, E2E: Cypress/Playwright) should be configured to generate reports conforming to this JSON schema.

CI/CD pipelines can parse these reports to determine build success/failure and track quality metrics over time.

UI testing dashboards (like the one potentially built for the Customizable UI Tests feature) can consume this JSON format to display results visually.

---

## 5. Implementation Notes

- **Schema Evolution:** This schema may evolve. Use versioning if significant backward-incompatible changes occur.
- **Tooling:** Libraries exist in most languages for generating JSON reports. Test runners often have plugins for standard formats (like JUnit XML), which might need adapters to convert to this JSON schema if direct generation isn't feasible.
- **Consistency:** Ensure all different types of tests (unit, integration, ethical, etc.) populate the relevant fields consistently.

---

## 6. Future Enhancements

- Add fields for linking test cases to requirements or user stories.
- Include code coverage metrics within the report.
- Define more specific schemas for `results[*].error`, `accessibilityViolations`, etc.
