# Logging Standards and Best Practices

---

## 1. Introduction

This document outlines the logging standards and best practices for the ThinkAlike project. Proper logging is essential for debugging, monitoring, auditing, and understanding system behavior in development and production environments. Following these guidelines ensures consistency and effectiveness across all components of the platform.

---

## 2. Logging Objectives

Effective logging in the ThinkAlike platform serves several key purposes:

* **Debugging:** Provide detailed context for troubleshooting issues

* **Monitoring:** Enable real-time system health observations

* **Auditing:** Record significant user actions and system events

* **Analytics:** Support data-driven insights about usage patterns

* **Security:** Track potential security incidents and unauthorized access attempts

---

## 3. Log Levels

Use appropriate log levels consistently across the codebase:

### 3.1 Level Definitions

* **ERROR:** System errors that prevent functionality from working correctly. Requires immediate attention.

  * Examples: Database connection failures, API integration failures, authentication errors

* **WARNING:** Unusual or unexpected events that don't cause system failure but may indicate problems.

  * Examples: Performance degradation, retry attempts, deprecated feature usage

* **INFO:** Normal but significant events that highlight application flow.

  * Examples: Service startup/shutdown, user registration, content creation

* **DEBUG:** Detailed information useful for debugging and development.

  * Examples: Function entry/exit, parameter values, state changes, detailed flow logic

* **TRACE:** Very detailed information primarily for development. Typically only enabled in development environments.

  * Examples: Loop iterations, detailed algorithm steps, function call frequency

### 3.2 Level Usage Guidelines

* Use **ERROR** sparingly for genuine errors, not for expected conditions

* Use **WARNING** for anomalies that don't prevent operation but should be investigated

* Use **INFO** for key lifecycle events and actions visible to users

* Use **DEBUG** for information helpful during development or detailed troubleshooting

* Configure production environments to typically log **INFO** and above

* Reserve **TRACE** for complex debugging scenarios, enabling temporarily as needed

---

## 4. Log Message Content

### 4.1 Message Structure

Each log message should include:

* **Timestamp:** When the event occurred (ISO 8601 format)

* **Level:** The log level (ERROR, WARNING, etc.)

* **Component/Module:** Which part of the system generated the log

* **Request ID/Correlation ID:** To trace requests across distributed systems

* **Message:** Clear, concise description of the event

* **Context:** Relevant data for understanding the event

### 4.2 Content Guidelines

* **Be Specific:** "User registration failed: Email already exists" instead of "Registration failed"

* **Include Key Data:** Log IDs, transaction references, and relevant parameters (sanitized)

* **Format for Readability:** Structure complex data as JSON for easy parsing

* **Be Concise:** Focus on essential information to avoid log bloat

### 4.3 Example Message Formats

```

# Backend (Python)

INFO [UserService] [req-abc123] User registered successfully: user_id=456, email="j***@example.com"

# Frontend (JavaScript)

ERROR [AuthComponent] [session-xyz789] Authentication failed: Invalid credentials after 3 attempts

```

---

## 5. Implementation

### 5.1 Backend (Python)

Use Python's built-in logging module with structured logging:

```python
import logging
import json
from contextvars import ContextVar

# Set up request_id context

request_id_var = ContextVar('request_id', default=None)

# Configure logger

logger = logging.getLogger('thinkalike')

def log_event(level, message, **context):
    """Log an event with structured context"""
    req_id = request_id_var.get()
    log_data = {
        'message': message,
        'request_id': req_id,

        **context
    }

    if level == 'error':
        logger.error(json.dumps(log_data))
    elif level == 'warning':
        logger.warning(json.dumps(log_data))
    else:
        logger.info(json.dumps(log_data))

# Usage example

log_event('info', 'User registered', user_id='123', email='masked@example.com')

```

### 5.2 Frontend (TypeScript)

Create a logging service that supports different environments:

```typescript
// logging-service.ts
export enum LogLevel {
  ERROR = 'ERROR',
  WARNING = 'WARNING',
  INFO = 'INFO',
  DEBUG = 'DEBUG'
}

class LoggingService {
  private sessionId: string;

  constructor() {
    this.sessionId = generateSessionId(); // implementation not shown
  }

  log(level: LogLevel, message: string, context?: Record<string, any>): void {
    const logData = {
      timestamp: new Date().toISOString(),
      level,
      message,
      sessionId: this.sessionId,
      ...context
    };

    // Development logging
    if (process.env.NODE_ENV === 'development') {
      this.logToConsole(level, message, logData);
    }

    // Production logging - send to backend or monitoring service
    if (process.env.NODE_ENV === 'production') {
      if (level === LogLevel.ERROR || level === LogLevel.WARNING) {
        this.sendToBackend(logData);
      }
    }
  }

  private logToConsole(level: LogLevel, message: string, data: any): void {
    switch (level) {
      case LogLevel.ERROR:
        console.error(`[${level}] ${message}`, data);
        break;
      case LogLevel.WARNING:
        console.warn(`[${level}] ${message}`, data);
        break;
      default:
        console.log(`[${level}] ${message}`, data);
    }
  }

  private sendToBackend(logData: any): void {
    // Implementation to send logs to backend
    fetch('/api/logs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(logData)
    }).catch(e => console.error('Failed to send log to server', e));
  }
}

export const logger = new LoggingService();

// Usage
import { logger, LogLevel } from './logging-service';
logger.log(LogLevel.INFO, 'User profile viewed', { userId: '123', section: 'preferences' });

```

---

## 6. Common Logging Scenarios

### 6.1 API Endpoints

Log the following for API endpoints:

* Request received (method, endpoint, client info)

* Response sent (status code, timing)

* Errors or exceptional conditions

```python
@app.get("/api/users/{user_id}")
async def get_user(user_id: str, request: Request):
    start_time = time.time()
    logger.info(f"Request received", endpoint="/api/users/{user_id}", method="GET")

    try:
        # Business logic...

        user = await user_service.get_user(user_id)

        elapsed = time.time() - start_time
        logger.info(f"Request completed",
                   endpoint="/api/users/{user_id}",
                   status_code=200,
                   duration_ms=int(elapsed * 1000))
        return user
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Error processing request",
                    endpoint="/api/users/{user_id}",
                    status_code=500,
                    error=str(e),
                    duration_ms=int(elapsed * 1000))
        raise

```

### 6.2 Background Tasks

Log the following for background tasks:

* Task start with parameters

* Task completion with results

* Task failures with detailed error information

* Progress for long-running tasks

### 6.3 Authentication Events

Log the following authentication events:

* Login attempts (success/failure)

* Password reset requests

* Permission changes

* Account lockouts

---

## 7. Security and Privacy Considerations

### 7.1 Sensitive Data

* **Never log:** Passwords, tokens, full credit card numbers, full SSNs

* **Mask sensitive data:** Email addresses, phone numbers, etc.

* **Use reference IDs:** Log reference IDs instead of actual data when possible

### 7.2 PII Handling

* Follow GDPR, CCPA, and other relevant privacy regulations

* Implement log retention policies that comply with legal requirements

* Consider logs as potentially containing PII when designing data deletion workflows

### 7.3 Log Security

* Protect log files with appropriate access controls

* Transmit logs securely when sending to external systems

* Consider encryption for highly sensitive logs

---

## 8. Log Management

### 8.1 Aggregation

* Use a centralized logging system (e.g., ELK stack, Graylog, SumoLogic, etc.)

* Configure log forwarding from all services to the central system

* Normalize log formats for consistent querying

### 8.2 Retention

* Define retention periods based on:

  * Regulatory requirements

  * Business needs

  * Storage constraints

* Implement automated archiving and deletion

### 8.3 Monitoring and Alerting

* Set up alerts for ERROR level logs

* Create dashboards for monitoring system health

* Implement automated scanning for security-relevant log patterns

---

## 9. Log Analysis Best Practices

* Use correlation IDs to track requests across distributed systems

* Create metrics from logs to monitor trends over time

* Regularly review logs to identify patterns and improvement opportunities

* Use log analysis to inform performance optimizations

---

By following these logging standards and practices, we ensure that ThinkAlike's logs provide maximum value for debugging, monitoring, and understanding system behavior while respecting security and privacy requirements.

---

**Document Details**

* Title: Logging Standards and Best Practices

* Type: Developer Guide

* Version: 1.0.0

* Last Updated: 2025-04-05

---

End of Logging Standards and Best Practices

---
