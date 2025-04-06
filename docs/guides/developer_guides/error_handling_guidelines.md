# Error Handling Guidelines

---

## 1. Introduction

This document outlines the standard approach for error handling in the ThinkAlike project. Proper error handling is crucial for building robust, maintainable software that provides good user experience even when things go wrong. These guidelines help ensure consistency across the codebase and make debugging easier for all team members.

---

## 2. General Principles

* **Be specific**: Errors should clearly describe what went wrong
* **Be actionable**: Errors should provide guidance on how to fix issues when possible
* **Be secure**: Never expose sensitive information in error messages to users
* **Be user-friendly**: Technical errors should be translated into user-friendly messages
* **Be traceable**: Errors should include information that helps with debugging

---

## 3. Backend Error Handling (Python)

### 3.1 Exception Hierarchy

ThinkAlike uses a custom exception hierarchy to organize different error types:

```python
# app/core/exceptions.py
class ThinkAlikeBaseException(Exception):
    """Base exception for all ThinkAlike errors"""
    def __init__(self, message, code=None, details=None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

# Authentication/Authorization Errors
class AuthenticationError(ThinkAlikeBaseException):
    """Raised when authentication fails"""
    pass

class PermissionDeniedError(ThinkAlikeBaseException):
    """Raised when user doesn't have permission"""
    pass

# Data Errors
class ValidationError(ThinkAlikeBaseException):
    """Raised when input data fails validation"""
    pass

class ResourceNotFoundError(ThinkAlikeBaseException):
    """Raised when a requested resource doesn't exist"""
    pass

class ConflictError(ThinkAlikeBaseException):
    """Raised when an operation would cause a conflict"""
    pass

# External Service Errors
class ExternalServiceError(ThinkAlikeBaseException):
    """Raised when an external service fails"""
    pass

# Business Logic Errors
class BusinessLogicError(ThinkAlikeBaseException):
    """Raised when business rules are violated"""
    pass
```

### 3.2 Raising Exceptions

When raising exceptions, include context that will help with debugging:

```python
# Example of raising a proper exception
def update_user_preferences(user_id, preferences):
    user = user_repository.get_by_id(user_id)

    if not user:
        raise ResourceNotFoundError(
            message=f"User not found",
            code="USER_NOT_FOUND",
            details={"user_id": user_id}
        )

    if not preferences_validator.is_valid(preferences):
        raise ValidationError(
            message="Invalid preference format",
            code="INVALID_PREFERENCES",
            details={"errors": preferences_validator.errors}
        )

    try:
        user_repository.update_preferences(user_id, preferences)
    except DatabaseError as e:
        raise ExternalServiceError(
            message="Failed to update user preferences",
            code="DB_ERROR",
            details={"original_error": str(e)}
        )
```

### 3.3 FastAPI Exception Handlers

Use FastAPI's exception handling to convert exceptions to appropriate HTTP responses:

```python
# app/api/error_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import *

async def authentication_error_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": {
                "code": exc.code or "AUTHENTICATION_ERROR",
                "message": exc.message,
                "details": exc.details
            }
        }
    )

async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": {
                "code": exc.code or "NOT_FOUND",
                "message": exc.message,
                "details": exc.details
            }
        }
    )

# Register in app startup
def register_exception_handlers(app):
    app.add_exception_handler(AuthenticationError, authentication_error_handler)
    app.add_exception_handler(PermissionDeniedError,
                             lambda req, exc: JSONResponse(
                                 status_code=status.HTTP_403_FORBIDDEN,
                                 content={"error": {
                                     "code": exc.code or "FORBIDDEN",
                                     "message": exc.message,
                                     "details": exc.details
                                 }}
                             ))
    app.add_exception_handler(ResourceNotFoundError, resource_not_found_handler)
    # Register other handlers...
```

---

## 4. Frontend Error Handling (TypeScript)

### 4.1 API Error Handling

Use a consistent approach to handle API errors:

```typescript
// src/utils/api-client.ts
interface ApiError {
  code: string;
  message: string;
  details?: Record<string, any>;
}

interface ApiErrorResponse {
  error: ApiError;
}

class ApiClient {
  async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    try {
      const response = await fetch(`/api/${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        // Convert API error responses to throw with our error structure
        const errorResponse = data as ApiErrorResponse;
        throw new ApiRequestError(
          errorResponse.error.message,
          errorResponse.error.code,
          response.status,
          errorResponse.error.details
        );
      }

      return data as T;
    } catch (error) {
      if (error instanceof ApiRequestError) {
        throw error;
      }

      // Network errors, etc.
      throw new ApiRequestError(
        'Failed to communicate with the server',
        'NETWORK_ERROR',
        0,
        { originalError: error }
      );
    }
  }
}

export class ApiRequestError extends Error {
  constructor(
    message: string,
    public code: string,
    public status: number,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = 'ApiRequestError';
  }
}

export const apiClient = new ApiClient();
```

### 4.2 React Error Handling

Use appropriate error handling patterns in React components:

```typescript
// Example React component with error handling
import React, { useState, useEffect } from 'react';
import { apiClient, ApiRequestError } from '../utils/api-client';
import { ErrorMessage, LoadingSpinner } from '../components/ui';
import { useToast } from '../hooks/useToast';

interface UserPreferencesProps {
  userId: string;
}

export const UserPreferences: React.FC<UserPreferencesProps> = ({ userId }) => {
  const [preferences, setPreferences] = useState<UserPreferenceData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const toast = useToast();

  useEffect(() => {
    const fetchPreferences = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await apiClient.request<UserPreferenceData>(`users/${userId}/preferences`);
        setPreferences(data);
      } catch (err) {
        if (err instanceof ApiRequestError) {
          if (err.status === 404) {
            setError('User preferences not found.');
          } else {
            setError(`Failed to load preferences: ${err.message}`);
          }
          // Log detailed error for debugging
          console.error('API Error:', err.code, err.message, err.details);
        } else {
          setError('An unexpected error occurred.');
          console.error('Unexpected error:', err);
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchPreferences();
  }, [userId]);

  const updatePreference = async (key: string, value: any) => {
    try {
      await apiClient.request(`users/${userId}/preferences`, {
        method: 'PATCH',
        body: JSON.stringify({ [key]: value }),
      });

      // Update local state to reflect the change
      setPreferences(prev => prev ? { ...prev, [key]: value } : null);

      toast.success('Preference updated successfully');
    } catch (err) {
      toast.error('Failed to update preference');
      console.error('Error updating preference:', err);
    }
  };

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  // Render preferences form...
};
```

### 4.3 Global Error Handling

Implement global error handlers for unhandled exceptions:

```typescript
// src/utils/error-boundary.tsx
import React, { ErrorInfo } from 'react';
import { logger } from '../utils/logger';

interface ErrorBoundaryProps {
  fallback?: React.ReactNode;
  children: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    // Log the error to our logging service
    logger.error('Component Error', {
      error: error.toString(),
      stack: error.stack,
      componentStack: info.componentStack
    });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-container">
          <h2>Something went wrong.</h2>
          <p>The team has been notified. Please try again later.</p>
          <button onClick={() => window.location.reload()}>
            Refresh Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

---

## 5. Error Logging

All errors should be logged appropriately to aid in debugging and monitoring:

### 5.1 Backend Logging

```python
# Logger setup and usage
import logging
from app.core.exceptions import ThinkAlikeBaseException

logger = logging.getLogger(__name__)

def process_data(data):
    try:
        # Process data...
        result = complex_operation(data)
        return result
    except ValidationError as e:
        # Expected errors - log at info or warning level
        logger.warning(
            "Validation error occurred",
            extra={
                "error_code": e.code,
                "details": e.details,
                "user_id": current_user.id
            }
        )
        raise
    except ThinkAlikeBaseException as e:
        # Application-specific errors - log appropriately
        logger.error(
            f"Application error: {e.message}",
            extra={
                "error_code": e.code,
                "details": e.details,
                "user_id": current_user.id
            }
        )
        raise
    except Exception as e:
        # Unexpected errors - always log as errors
        logger.exception(
            "Unexpected error in data processing",
            extra={"data_id": data.id if hasattr(data, 'id') else None}
        )
        raise ExternalServiceError(
            message="An unexpected error occurred",
            code="UNEXPECTED_ERROR",
            details={"original_error": str(e)}
        )
```

### 5.2 Frontend Logging

```typescript
// Error logging in frontend
import { logger } from '../utils/logger';

export async function fetchUserData(userId: string) {
  try {
    // Fetch user data
  } catch (error) {
    if (error instanceof ApiRequestError) {
      // Log API errors with context
      logger.error('API error when fetching user data', {
        userId,
        errorCode: error.code,
        status: error.status,
        message: error.message
      });
    } else {
      // Log unexpected errors
      logger.error('Unexpected error when fetching user data', {
        userId,
        error: error instanceof Error ? error.message : String(error)
      });
    }
    throw error; // Re-throw for component handling
  }
}
```

---

## 6. HTTP Status Codes and Error Response Format

### 6.1 HTTP Status Codes

Use appropriate HTTP status codes for API responses:

* **200 OK**: Successful request
* **201 Created**: Resource successfully created
* **400 Bad Request**: Invalid input, validation errors
* **401 Unauthorized**: Authentication required or failed
* **403 Forbidden**: Authenticated but lacking permissions
* **404 Not Found**: Resource not found
* **409 Conflict**: Request conflicts with current state
* **422 Unprocessable Entity**: Validation passed but semantic errors exist
* **429 Too Many Requests**: Rate limit exceeded
* **500 Internal Server Error**: Unexpected server error
* **503 Service Unavailable**: Service temporarily unavailable

### 6.2 Standard Error Response Format

All API error responses should follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      "field1": "Specific error about field1",
      "field2": "Specific error about field2"
    }
  }
}
```

---

## 7. Error Translation for End Users

Technical errors must be translated into user-friendly messages:

### 7.1 Backend Translation

```python
# Example of error translation middleware for FastAPI
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class ErrorTranslationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Only process error responses
        if response.status_code >= 400:
            body = await response.body()

            # Parse the JSON body
            import json
            try:
                data = json.loads(body)
                if "error" in data and "code" in data["error"]:
                    # Translate the error based on code
                    user_message = ERROR_TRANSLATIONS.get(
                        data["error"]["code"],
                        "An unexpected error occurred. Please try again later."
                    )

                    # Add user-friendly message
                    data["error"]["user_message"] = user_message

                    # Create new response with translated error
                    return Response(
                        content=json.dumps(data),
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type=response.media_type
                    )
            except json.JSONDecodeError:
                pass

        return response

# Define error translations
ERROR_TRANSLATIONS = {
    "AUTHENTICATION_ERROR": "Please log in to continue.",
    "USER_NOT_FOUND": "This user could not be found.",
    "INVALID_PREFERENCES": "The preferences you provided are not valid.",
    # ...more translations
}
```

### 7.2 Frontend Translation

```typescript
// Frontend error translation
const USER_ERROR_MESSAGES: Record<string, string> = {
  'NETWORK_ERROR': 'Unable to connect to the server. Please check your internet connection.',
  'AUTHENTICATION_ERROR': 'Your session has expired. Please log in again.',
  'PERMISSION_DENIED': 'You don\'t have permission to perform this action.',
  'USER_NOT_FOUND': 'User not found.',
  // More error translations...
};

function getErrorMessage(error: ApiRequestError): string {
  // First check if we have a user_message from the backend
  if (error.details?.user_message) {
    return error.details.user_message;
  }

  // Otherwise look up the error code in our translations
  const defaultMessage = 'Something went wrong. Please try again later.';
  return USER_ERROR_MESSAGES[error.code] || error.message || defaultMessage;
}
```

---

## 8. Error Prevention Strategies

Beyond handling errors when they occur, focus on preventing them:

* **Input Validation**: Validate all user input thoroughly
* **Type Safety**: Leverage TypeScript's static typing
* **Defensive Programming**: Check for null/undefined values
* **API Contracts**: Use OpenAPI/Swagger for API definitions
* **Feature Flags**: Roll out high-risk features gradually
* **Monitoring**: Use alerts to catch errors quickly

---

## 9. Testing Error Scenarios

Always test error handling explicitly:

### 9.1 Backend Testing

```python
# Example error handling test for backend
def test_user_not_found_returns_404():
    # Setup
    non_existent_id = "user-that-does-not-exist"

    # Execute
    response = client.get(f"/api/users/{non_existent_id}")

    # Verify
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "USER_NOT_FOUND"
```

### 9.2 Frontend Testing

```typescript
// Example error handling test for React component
test('renders error message when API call fails', async () => {
  // Mock API to throw an error
  apiClient.request = jest.fn().mockRejectedValue(
    new ApiRequestError('User not found', 'USER_NOT_FOUND', 404)
  );

  render(<UserProfile userId="123" />);

  // Check loading state first
  expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();

  // Wait for error state
  const errorMessage = await screen.findByText(/user not found/i);
  expect(errorMessage).toBeInTheDocument();
});
```

---

By following these error handling guidelines, ThinkAlike ensures consistent, informative error handling that improves both developer and user experiences while making debugging and maintenance easier.
