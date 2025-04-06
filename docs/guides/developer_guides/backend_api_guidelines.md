# Backend API Development Guidelines

---

## 1. Introduction

This document outlines the backend API development standards and best practices for the ThinkAlike project. Well-designed APIs are essential for system integration, developer productivity, and creating reliable experiences for both internal and external clients. These guidelines ensure consistency across all ThinkAlike APIs and provide a framework for building maintainable, secure, and performant services.

---

## 2. API Design Principles

### 2.1 Core Principles

* **REST-first**: Follow RESTful design principles where appropriate
* **Resource-Oriented**: Model APIs around resources and their relationships
* **Consistency**: Maintain consistent patterns across all endpoints
* **Simplicity**: Prefer simplicity over complexity in design
* **Self-Documenting**: Design APIs to be intuitive and self-explanatory
* **Evolution**: Support versioning and backward compatibility
* **Security**: Implement proper authentication and authorization

### 2.2 API Styles

ThinkAlike uses the following API styles:

* **RESTful APIs**: Primary style for resource-based operations
* **GraphQL**: For complex data requirements with nested relationships
* **WebSockets**: For real-time bidirectional communication
* **Event-Driven APIs**: For asynchronous processing and notifications

---

## 3. RESTful API Design

### 3.1 URL Structure

* Use **plural nouns** for resource collections (`/users`, `/articles`)
* Use **resource identifiers** for specific resources (`/users/123`)
* Use **sub-resources** for relationships (`/users/123/preferences`)
* Use **kebab-case** for multi-word resource names (`/account-settings`)
* Avoid deep nesting (no more than 2-3 levels)

```
# Good URL structure examples
GET /api/v1/users                 # Get all users
GET /api/v1/users/123             # Get specific user
POST /api/v1/users                # Create new user
PUT /api/v1/users/123             # Update user
DELETE /api/v1/users/123          # Delete user
GET /api/v1/users/123/preferences # Get user preferences
```

### 3.2 HTTP Methods

Use HTTP methods appropriately:

| Method | Purpose | Examples |
|--------|---------|----------|
| GET | Retrieve data | `GET /users`, `GET /users/123` |
| POST | Create resources or trigger actions | `POST /users`, `POST /users/import` |
| PUT | Replace a resource entirely | `PUT /users/123` |
| PATCH | Partially update a resource | `PATCH /users/123` |
| DELETE | Remove a resource | `DELETE /users/123` |
| HEAD | Get headers only (like GET without body) | `HEAD /users/123` |
| OPTIONS | Get supported methods for a resource | `OPTIONS /users` |

### 3.3 Query Parameters

* Use for **filtering**: `GET /users?status=active`
* Use for **pagination**: `GET /users?page=2&per_page=25`
* Use for **sorting**: `GET /users?sort=last_name&order=asc`
* Use for **field selection**: `GET /users?fields=id,username,email`
* Use for **searching**: `GET /users?q=smith`

```python
# Example query parameter handling in FastAPI
from fastapi import FastAPI, Query
from enum import Enum
from typing import List, Optional

app = FastAPI()

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

@app.get("/users")
async def get_users(
    status: Optional[str] = None,
    page: int = Query(1, gt=0),
    per_page: int = Query(25, gt=0, le=100),
    sort: Optional[str] = None,
    order: SortOrder = SortOrder.asc,
    fields: Optional[List[str]] = Query(None),
    q: Optional[str] = None
):
    """
    Get users with filtering, pagination, sorting, and search.
    """
    # Build query filters based on parameters
    query_filters = {}
    if status:
        query_filters["status"] = status

    # Apply search if provided
    search_condition = None
    if q:
        search_condition = {"$or": [
            {"first_name": {"$regex": q, "$options": "i"}},
            {"last_name": {"$regex": q, "$options": "i"}},
            {"email": {"$regex": q, "$options": "i"}},
        ]}

    # Calculate pagination
    skip = (page - 1) * per_page

    # Build sort condition
    sort_condition = {}
    if sort:
        sort_direction = 1 if order == SortOrder.asc else -1
        sort_condition = {sort: sort_direction}

    # Execute query with all conditions
    # (Pseudocode - actual implementation would use your database ORM)
    users = db.users.find(
        {**query_filters, **search_condition} if search_condition else query_filters,
        skip=skip,
        limit=per_page,
        sort=sort_condition or None
    )

    # Apply field selection if specified
    if fields:
        projection = {field: 1 for field in fields}
        users = users.project(projection)

    # Count total for pagination metadata
    total = db.users.count({**query_filters, **search_condition} if search_condition else query_filters)

    return {
        "data": list(users),
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
        }
    }
```

### 3.4 Response Format

Use a consistent response format:

```json
// Success response format (GET collection)
{
  "data": [
    {
      "id": "123",
      "type": "user",
      "attributes": {
        "username": "johndoe",
        "email": "john@example.com",
        "created_at": "2023-01-15T14:30:00Z"
      },
      "relationships": {
        "preferences": {
          "links": {
            "self": "/api/v1/users/123/relationships/preferences",
            "related": "/api/v1/users/123/preferences"
          }
        }
      }
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 25,
    "total": 150,
    "pages": 6
  },
  "links": {
    "self": "/api/v1/users?page=1&per_page=25",
    "first": "/api/v1/users?page=1&per_page=25",
    "last": "/api/v1/users?page=6&per_page=25",
    "next": "/api/v1/users?page=2&per_page=25",
    "prev": null
  }
}

// Error response format
{
  "errors": [
    {
      "status": "400",
      "code": "invalid_parameter",
      "title": "Invalid Parameter",
      "detail": "The 'email' parameter must be a valid email address.",
      "source": {
        "parameter": "email"
      }
    }
  ]
}
```

### 3.5 Status Codes

Use appropriate HTTP status codes:

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST that creates a resource |
| 204 | No Content | Successful DELETE or PUT with no response body |
| 400 | Bad Request | Invalid input, validation errors |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authentication succeeded but insufficient permissions |
| 404 | Not Found | Resource not found |
| 405 | Method Not Allowed | Method not supported for this resource |
| 409 | Conflict | Request conflicts with current state |
| 422 | Unprocessable Entity | Validation failed, semantically incorrect |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Service temporarily unavailable |

```python
# Example status code usage in Flask
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = find_user(user_id)
    if not user:
        raise NotFound("User not found")
    return jsonify({"data": user_to_dict(user)}), 200

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validate input
    if not data or not data.get('email') or not data.get('username'):
        return jsonify({
            "errors": [{
                "status": "400",
                "code": "missing_fields",
                "title": "Missing Required Fields",
                "detail": "Username and email are required fields."
            }]
        }), 400

    # Check for existing user
    existing_user = find_user_by_email(data['email'])
    if existing_user:
        return jsonify({
            "errors": [{
                "status": "409",
                "code": "email_exists",
                "title": "Email Already Exists",
                "detail": "A user with this email already exists."
            }]
        }), 409

    # Create user
    new_user = create_user_in_db(data)

    # Return created user with 201 status
    return jsonify({"data": user_to_dict(new_user)}), 201
```

---

## 4. API Versioning

### 4.1 Versioning Strategies

ThinkAlike uses **URI path versioning** as the primary versioning strategy:

```
/api/v1/users
/api/v2/users
```

### 4.2 Version Compatibility

* **Major versions** (v1, v2): May contain breaking changes
* **Minor versions**: Must be backward compatible
* Support at least **one previous major version** after a new version is released
* Include **deprecation notices** in headers for outdated endpoints
* Set a **deprecation timeline** for retiring old versions

```python
# Example versioning in Flask with Blueprints
from flask import Flask, Blueprint, jsonify

app = Flask(__name__)

# Version 1 blueprint
v1_blueprint = Blueprint('v1', __name__, url_prefix='/api/v1')

@v1_blueprint.route('/users', methods=['GET'])
def get_users_v1():
    # V1 implementation
    users = get_users_from_db()
    return jsonify({"users": [{"id": u.id, "name": u.name} for u in users]})

# Version 2 blueprint
v2_blueprint = Blueprint('v2', __name__, url_prefix='/api/v2')

@v2_blueprint.route('/users', methods=['GET'])
def get_users_v2():
    # V2 implementation with enhanced output
    users = get_users_from_db()
    return jsonify({
        "data": [
            {
                "id": str(u.id),
                "type": "user",
                "attributes": {
                    "username": u.username,
                    "name": u.name,
                    "email": u.email,
                    "created_at": u.created_at.isoformat()
                }
            } for u in users
        ],
        "meta": {"count": len(users)}
    })

# Register blueprints
app.register_blueprint(v1_blueprint)
app.register_blueprint(v2_blueprint)

# Add deprecation notice for v1
@app.after_request
def add_deprecation_headers(response):
    if request.path.startswith('/api/v1/'):
        response.headers['Deprecation'] = 'true'
        response.headers['Sunset'] = 'Wed, 01 Jan 2024 23:59:59 GMT'
        response.headers['Link'] = '</api/v2/users>; rel="successor-version"'
    return response
```

---

## 5. Authentication and Authorization

### 5.1 Authentication Methods

* **JWT-based authentication**: Primary method for most APIs
* **API Keys**: For service-to-service or external integrations
* **OAuth 2.0**: For third-party application access
* **OpenID Connect**: For federated login flows

```python
# Example JWT authentication in FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel

# Setup
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "YOUR_SECRET_KEY"  # In production, load from secure environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

# Function to create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(token_data.username)  # Function to retrieve user from db
    if user is None:
        raise credentials_exception

    return user

# Login endpoint to get token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoint example
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### 5.2 Authorization

* Use **role-based access control (RBAC)** for authorization
* Implement **permission-based checks** for fine-grained control
* Define **scopes** for OAuth-based access
* Validate authorization at the API gateway or middleware level

```python
# Example RBAC implementation
from enum import Enum, auto
from functools import wraps
from flask import g, request, abort

class Role(Enum):
    GUEST = auto()
    USER = auto()
    EDITOR = auto()
    ADMIN = auto()

# Permission mapping
ROLE_PERMISSIONS = {
    Role.GUEST: ['read:public'],
    Role.USER: ['read:public', 'read:user', 'write:user'],
    Role.EDITOR: ['read:public', 'read:user', 'write:user', 'write:content'],
    Role.ADMIN: ['read:public', 'read:user', 'write:user', 'write:content', 'admin:*'],
}

def has_permission(user, permission):
    """Check if user has the required permission."""
    if not user or not user.role:
        return False

    # Get permissions for user's role
    role_permissions = ROLE_PERMISSIONS.get(user.role, [])

    # Check for specific permission
    if permission in role_permissions:
        return True

    # Check for wildcard permissions
    for p in role_permissions:
        if p.endswith(':*'):
            base = p[:-1]
            if permission.startswith(base):
                return True

    return False

def require_permission(permission):
    """Decorator to require a specific permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get current user from context (set by auth middleware)
            current_user = g.user

            if not has_permission(current_user, permission):
                abort(403, description=f"Permission denied: {permission} required")

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Usage example
@app.route('/api/v1/articles/<int:article_id>', methods=['PUT'])
@require_permission('write:content')
def update_article(article_id):
    # This endpoint is protected and requires 'write:content' permission
    # Implementation...
    return jsonify({"message": "Article updated"})
```

---

## 6. API Documentation

### 6.1 Documentation Standards

* Document **all** endpoints with:
  * **Description**: Clear explanation of the endpoint's purpose
  * **Parameters**: All query parameters, path variables, and request body fields
  * **Responses**: All possible response codes and bodies
  * **Authentication**: Required permissions or scopes
  * **Examples**: Request and response examples

### 6.2 OpenAPI Specification

Use OpenAPI (formerly Swagger) for API documentation:

```python
# Example FastAPI with automatic OpenAPI docs
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

app = FastAPI(
    title="ThinkAlike API",
    description="API for ThinkAlike platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class UserBase(BaseModel):
    username: str = Field(..., description="Unique username", example="johndoe")
    email: str = Field(..., description="User email address", example="john@example.com")
    full_name: Optional[str] = Field(None, description="User's full name", example="John Doe")

class UserCreate(UserBase):
    password: str = Field(..., description="User password (will be hashed)", example="securepassword123")

class User(UserBase):
    id: int = Field(..., description="User ID")
    role: UserRole = Field(default=UserRole.USER, description="User role")
    is_active: bool = Field(default=True, description="Whether the user is active")

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "role": "user",
                "is_active": True
            }
        }

@app.post("/users/", response_model=User, status_code=201,
          summary="Create new user",
          description="Create a new user with the provided details")
async def create_user(user: UserCreate = Body(..., description="User data")):
    """
    Create a new user in the system.

    - **username**: Required. Must be unique.
    - **email**: Required. Valid email format.
    - **full_name**: Optional. User's full name.
    - **password**: Required. Will be securely hashed.

    Returns the created user object with generated ID.
    """
    # Implementation...
    return {"id": 123, **user.dict(exclude={"password"}), "role": UserRole.USER, "is_active": True}

@app.get("/users/{user_id}", response_model=User,
         summary="Get user by ID",
         description="Retrieve a specific user by their ID")
async def read_user(
    user_id: int = Path(..., description="The ID of the user to retrieve", gt=0, example=123)
):
    """
    Retrieve a user by their ID.

    - **user_id**: Required path parameter. Must be a positive integer.

    Returns the user object if found.
    """
    # Implementation...
    return {
        "id": user_id,
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "role": UserRole.USER,
        "is_active": True
    }
```

### 6.3 Documentation as Code

* Maintain API documentation alongside code
* Use tools that generate documentation from code comments and annotations
* Update documentation in the same PR as code changes
* Run documentation tests in CI/CD pipeline

---

## 7. Error Handling

### 7.1 Error Response Format

Use a consistent error response format:

```json
{
  "errors": [
    {
      "status": "400",
      "code": "validation_error",
      "title": "Validation Error",
      "detail": "The email field must be a valid email address.",
      "source": {
        "pointer": "/data/attributes/email"
      },
      "meta": {
        "validation": {
          "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        }
      }
    }
  ]
}
```

### 7.2 Error Codes

Define application-specific error codes:

```python
# Example error code enum
from enum import Enum

class ErrorCode(Enum):
    # Authentication and authorization errors (1000-1999)
    INVALID_CREDENTIALS = "1001"
    TOKEN_EXPIRED = "1002"
    INSUFFICIENT_PERMISSIONS = "1003"

    # Validation errors (2000-2999)
    VALIDATION_ERROR = "2001"
    INVALID_FORMAT = "2002"
    REQUIRED_FIELD_MISSING = "2003"

    # Resource errors (3000-3999)
    RESOURCE_NOT_FOUND = "3001"
    RESOURCE_ALREADY_EXISTS = "3002"
    RESOURCE_CONFLICT = "3003"

    # Server errors (5000-5999)
    INTERNAL_ERROR = "5001"
    DATABASE_ERROR = "5002"
    EXTERNAL_SERVICE_ERROR = "5003"
```

### 7.3 Exception Handling

Implement centralized exception handling:

```python
# Example global exception handler in Flask
from flask import Flask, jsonify, request
import traceback
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base class for API exceptions."""
    def __init__(self, code, title, detail, status_code=400, source=None, meta=None):
        self.code = code
        self.title = title
        self.detail = detail
        self.status_code = status_code
        self.source = source
        self.meta = meta

@app.errorhandler(APIError)
def handle_api_error(error):
    error_response = {
        "errors": [{
            "status": str(error.status_code),
            "code": error.code,
            "title": error.title,
            "detail": error.detail,
        }]
    }

    if error.source:
        error_response["errors"][0]["source"] = error.source

    if error.meta:
        error_response["errors"][0]["meta"] = error.meta

    return jsonify(error_response), error.status_code

@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({
        "errors": [{
            "status": "404",
            "code": "not_found",
            "title": "Not Found",
            "detail": f"The requested URL {request.path} was not found on the server."
        }]
    }), 404

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    # Log the full error with traceback
    logger.error(f"Unexpected error: {str(error)}\n{traceback.format_exc()}")

    # Return generic error to user
    return jsonify({
        "errors": [{
            "status": "500",
            "code": "internal_server_error",
            "title": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again later."
        }]
    }), 500

# Example usage
@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = find_user(user_id)
    if not user:
        # Raise specific error
        raise APIError(
            code="user_not_found",
            title="User Not Found",
            detail=f"User with ID {user_id} could not be found.",
            status_code=404,
            source={"parameter": "user_id"}
        )
    return jsonify({"data": user})
```

---

## 8. API Performance and Optimization

### 8.1 Response Optimization

* Implement **pagination** for collection endpoints
* Support **field selection** to reduce payload size
* Enable **compression** (gzip, Brotli) for responses
* Use efficient **serialization** formats

```python
# Example pagination implementation in Django REST Framework
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'per_page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'meta': {
                'page': self.page.number,
                'per_page': self.page.paginator.per_page,
                'pages': self.page.paginator.num_pages,
                'total': self.page.paginator.count
            },
            'links': {
                'self': self.request.build_absolute_uri(),
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'first': self.get_first_link(),
                'last': self.get_last_link(),
            }
        })

    def get_first_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        return remove_query_param(url, self.page_query_param)

    def get_last_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return replace_query_param(url, self.page_query_param, page_number)
```

### 8.2 Caching

* Implement **response caching** for frequently accessed data
* Use **ETags** or **Last-Modified** headers for conditional requests
* Apply **cache control** headers appropriately
* Consider **client-side caching** strategies

```python
# Example caching implementation in Flask
from flask import Flask, jsonify, request, make_response
from werkzeug.http import http_date, parse_date
from functools import wraps
import hashlib
import time

app = Flask(__name__)

def etag_for_data(data):
    """Generate ETag for data."""
    data_str = str(data).encode('utf-8')
    return hashlib.md5(data_str).hexdigest()

def cache_control(max_age=300, public=True):
    """
    Add Cache-Control headers to response.

    :param max_age: Maximum age in seconds
    :param public: Whether the response is cacheable by shared caches
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)

            # Add cache control directives
            directives = []
            if public:
                directives.append('public')
            else:
                directives.append('private')

            directives.append(f'max-age={max_age}')

            # Add headers to response
            if isinstance(response, dict):
                response = jsonify(response)

            response.headers['Cache-Control'] = ', '.join(directives)
            return response
        return decorated_function
    return decorator

def conditional_request(f):
    """
    Handle conditional requests with ETags.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Execute the original function to get data
        data = f(*args, **kwargs)

        # Generate ETag for response data
        etag = etag_for_data(data)

        # Check If-None-Match header for conditional GET
        if_none_match = request.headers.get('If-None-Match')
        if if_none_match and if_none_match == etag:
            return '', 304  # Not Modified

        # Create response with ETag
        response = make_response(jsonify(data))
        response.headers['ETag'] = etag
        response.headers['Last-Modified'] = http_date(time.time())

        return response
    return decorated_function

# Usage example
@app.route('/api/v1/popular-articles')
@cache_control(max_age=600)  # Cache for 10 minutes
@conditional_request
def get_popular_articles():
    # This data would typically come from a database
    articles = [
        {"id": 1, "title": "Introduction to API Design"},
        {"id": 2, "title": "RESTful Best Practices"},
        {"id": 3, "title": "GraphQL vs REST"}
    ]
    return {"data": articles}
```

### 8.3 Rate Limiting

* Implement **rate limiting** to prevent abuse
* Use **token bucket** or similar algorithms
* Include rate limit information in headers
* Design different limits for different client types

```python
# Example rate limiting using Flask-Limiter
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Define rate limit functions based on client type
def get_client_type():
    api_key = request.headers.get('X-API-Key', '')
    if api_key.startswith('partner_'):
        return 'partner'
    elif api_key:
        return 'registered'
    return 'anonymous'

def limit_by_client_type():
    client_type = get_client_type()
    limits = {
        'partner': '1000 per minute',
        'registered': '100 per minute',
        'anonymous': '10 per minute'
    }
    return limits.get(client_type, '5 per minute')

# Initialize limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379",
    strategy="fixed-window"  # or "moving-window", "elastic-window"
)

# Global rate limit
@app.route('/api/v1/public-data')
@limiter.limit("100 per hour")
def public_data():
    return jsonify({"data": "Public information"})

# Rate limit by client type
@app.route('/api/v1/users')
@limiter.limit(limit_by_client_type)
def get_users():
    # Get users based on client type permissions
    client_type = get_client_type()
    # Implementation...
    return jsonify({"data": "User data"})

# Handle rate limit exceeded
@app.errorhandler(429)
def handle_rate_limit_exceeded(e):
    return jsonify({
        "errors": [{
            "status": "429",
            "code": "rate_limit_exceeded",
            "title": "Rate Limit Exceeded",
            "detail": str(e.description),
            "meta": {
                "retry_after": e.retry_after
            }
        }]
    }), 429
```

---

## 9. API Testing

### 9.1 API Testing Strategy

* Implement **automated tests** for all endpoints
* Test **positive scenarios** and **error cases**
* Verify **authentication** and **authorization**
* Include **performance** and **load testing**

### 9.2 Unit Testing

```python
# Example API unit tests using pytest and Flask
import pytest
import json
from app import create_app
from app.models import db, User

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })

    # Set up the database
    with app.app_context():
        db.create_all()

    yield app

    # Clean up
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client for the application."""
    return app.test_client()

@pytest.fixture
def auth_headers():
    """Authentication headers."""
    return {
        'Authorization': 'Bearer test-token',
        'Content-Type': 'application/json'
    }

def test_get_users(client, auth_headers):
    """Test getting users endpoint."""
    response = client.get('/api/v1/users', headers=auth_headers)
    data = json.loads(response.data)

    # Verify response code and structure
    assert response.status_code == 200
    assert 'data' in data
    assert isinstance(data['data'], list)

def test_create_user_success(client, auth_headers):
    """Test creating user successfully."""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword123'
    }

    response = client.post(
        '/api/v1/users',
        headers=auth_headers,
        data=json.dumps(user_data)
    )
    data = json.loads(response.data)

    # Verify response
    assert response.status_code == 201
    assert 'data' in data
    assert data['data']['username'] == user_data['username']
    assert data['data']['email'] == user_data['email']
    assert 'id' in data['data']
    assert 'password' not in data['data']

def test_create_user_validation_error(client, auth_headers):
    """Test user creation with validation error."""
    # Missing required fields
    user_data = {
        'username': 'testuser'
    }

    response = client.post(
        '/api/v1/users',
        headers=auth_headers,
        data=json.dumps(user_data)
    )
    data = json.loads(response.data)

    # Verify error response
    assert response.status_code == 400
    assert 'errors' in data
    assert isinstance(data['errors'], list)
    assert data['errors'][0]['code'] == 'validation_error'
```

### 9.3 Integration Testing

```python
# Example API integration tests
import pytest
import requests
import jwt
import time

API_URL = 'http://localhost:8000/api/v1'
TEST_USER = {'username': 'integrationtest', 'password': 'testpassword'}

@pytest.fixture
def auth_token():
    """Get authentication token for test user."""
    response = requests.post(f'{API_URL}/auth/login', json=TEST_USER)
    assert response.status_code == 200
    return response.json()['access_token']

def test_user_workflow(auth_token):
    """Test complete user workflow."""
    headers = {'Authorization': f'Bearer {auth_token}'}

    # 1. Create a new user
    new_user = {
        'username': f'testuser{int(time.time())}',
        'email': f'test{int(time.time())}@example.com',
        'password': 'SecurePass123!'
    }

    response = requests.post(f'{API_URL}/users', headers=headers, json=new_user)
    assert response.status_code == 201
    user_data = response.json()['data']
    user_id = user_data['id']

    # 2. Get the created user
    response = requests.get(f'{API_URL}/users/{user_id}', headers=headers)
    assert response.status_code == 200
    assert response.json()['data']['username'] == new_user['username']

    # 3. Update the user
    update_data = {'full_name': 'Test User'}
    response = requests.patch(
        f'{API_URL}/users/{user_id}',
        headers=headers,
        json=update_data
    )
    assert response.status_code == 200
    assert response.json()['data']['full_name'] == update_data['full_name']

    # 4. Delete the user
    response = requests.delete(f'{API_URL}/users/{user_id}', headers=headers)
    assert response.status_code == 204

    # 5. Verify user is gone
    response = requests.get(f'{API_URL}/users/{user_id}', headers=headers)
    assert response.status_code == 404
```

### 9.4 Contract Testing

```python
# Example Pact consumer test
import pytest
from pact import Consumer, Provider
from api_client import ApiClient

@pytest.fixture
def pact():
    return Consumer('UserServiceClient').has_pact_with(
        Provider('UserService'),
        pact_dir='./pacts',
        host_name='localhost',
        port=1234
    )

def test_get_user(pact):
    # Define expected interaction
    pact.given(
        'a user with ID 123 exists'
    ).upon_receiving(
        'a request for user 123'
    ).with_request(
        'GET', '/api/v1/users/123',
        headers={'Authorization': 'Bearer token'}
    ).will_respond_with(
        200,
        headers={'Content-Type': 'application/json'},
        body={
            'data': {
                'id': '123',
                'type': 'user',
                'attributes': {
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'full_name': 'Test User'
                }
            }
        }
    )

    # Test with the mock service
    with pact:
        api_client = ApiClient(base_url='http://localhost:1234', auth_token='token')
        user = api_client.get_user('123')

        assert user['id'] == '123'
        assert user['username'] == 'testuser'
        assert user['email'] == 'test@example.com'
```

---

## 10. API Security

### 10.1 Security Headers

* Set appropriate security headers for all responses:
  * **Content-Security-Policy**: Prevent XSS attacks
  * **Strict-Transport-Security**: Enforce HTTPS
  * **X-Content-Type-Options**: Prevent MIME type sniffing
  * **X-Frame-Options**: Prevent clickjacking
  * **X-XSS-Protection**: Enable browser XSS filtering

```python
# Example security headers middleware for Flask
from flask import Flask, request

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    """Add security headers to response."""
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

### 10.2 Input Validation

* Validate **all** input data
* Use **schema validation** libraries
* Sanitize data to prevent injection attacks
* Apply strict type checking

```python
# Example request validation using Pydantic and FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re

app = FastAPI()

class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50,
                         description="User's unique username")
    email: EmailStr = Field(..., description="User's email address")
    full_name: Optional[str] = Field(None, max_length=100,
                                   description="User's full name")
    password: str = Field(..., min_length=8, description="User's password")

    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must be alphanumeric with underscores only')
        return v

    @validator('password')
    def password_strength(cls, v):
        # Check for at least one uppercase, one lowercase, one digit
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', v):
            raise ValueError(
                'Password must contain at least one uppercase letter, '
                'one lowercase letter, and one number'
            )
        return v

@app.post("/users/")
async def create_user(user: CreateUserRequest):
    # Input is already validated by Pydantic
    # Implementation...
    return {"id": 123, **user.dict(exclude={"password"})}
```

### 10.3 CORS Configuration

* Implement restrictive CORS policies
* Only allow necessary origins, methods, and headers
* Use **credentials** mode carefully
* Set appropriate **preflight** cache duration

```python
# Example CORS configuration in Flask
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS
CORS(app,
     resources={r"/api/*": {
         "origins": ["https://thinkalike.com", "https://app.thinkalike.com"],
         "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
         "expose_headers": ["X-Total-Count", "X-Pagination-Pages"],
         "max_age": 86400,  # 24 hours
         "supports_credentials": True
     }})

@app.route('/api/v1/users')
def get_users():
    # Implementation...
    return {"data": [...]}
```

---

## 11. API Evolution and Maintenance

### 11.1 Breaking Changes

* Avoid breaking changes when possible
* When necessary, introduce them in new major versions
* Provide **deprecation notices** before removing features
* Support old versions for a reasonable transition period

### 11.2 Feature Flags

* Use feature flags for gradual rollouts
* Test new features with limited users
* Toggle features based on client capabilities
* Use flags for A/B testing

```python
# Example feature flag implementation
from flask import Flask, request, jsonify
import os
import redis

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def feature_enabled(feature_name, user_id=None):
    """
    Check if a feature is enabled.

    :param feature_name: Name of the feature
    :param user_id: Optional user ID for user-specific flags
    :return: Boolean indicating if feature is enabled
    """
    # Check environment override (useful for local development)
    env_flag = os.environ.get(f'FEATURE_{feature_name.upper()}')
    if env_flag is not None:
        return env_flag.lower() == 'true'

    # Check user-specific flag
    if user_id:
        user_specific = redis_client.get(f'feature:{feature_name}:user:{user_id}')
        if user_specific is not None:
            return user_specific == b'1'

    # Check percentage rollout
    rollout_pct = redis_client.get(f'feature:{feature_name}:percentage')
    if rollout_pct is not None:
        rollout_pct = int(rollout_pct)
        if rollout_pct == 100:
            return True
        elif rollout_pct == 0:
            return False
        elif user_id:
            # Deterministic result based on user_id
            import hashlib
            user_hash = int(hashlib.md5(str(user_id).encode()).hexdigest(), 16)
            return (user_hash % 100) < rollout_pct

    # Check global flag
    global_flag = redis_client.get(f'feature:{feature_name}')
    if global_flag is not None:
        return global_flag == b'1'

    # Default to disabled
    return False

@app.route('/api/v1/content/<content_id>')
def get_content(content_id):
    # Get current user from authentication
    current_user = get_current_user_from_auth()
    user_id = current_user.id if current_user else None

    # Get basic content
    content = get_content_from_db(content_id)

    # Add enhanced content if feature flag is enabled
    if feature_enabled('enhanced_content', user_id):
        content['enhanced_data'] = get_enhanced_content(content_id)

    return jsonify({"data": content})
```

### 11.3 API Monitoring

* Monitor **request rates** and **response times**
* Track **error rates** by endpoint
* Set up **alerts** for unusual patterns
* Use **distributed tracing** for request flows

```python
# Example API monitoring with Prometheus metrics in Flask
from flask import Flask, request
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP Request Latency',
    ['method', 'endpoint']
)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    # Skip metrics endpoint itself
    if request.path != '/metrics':
        # Extract path template (replace IDs with placeholders)
        endpoint = request.path
        for rule in app.url_map.iter_rules():
            if rule.match(request.path):
                endpoint = rule.rule
                break

        # Record request count
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()

        # Record request latency
        latency = time.time() - request.start_time
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(latency)

    return response

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}
```

---

## 12. API Governance

### 12.1 API Review Process

* Create an **API review** checklist
* Conduct reviews for new endpoints and changes
* Consider **security**, **usability**, and **performance**
* Ensure consistency with API standards

### 12.2 API Style Guide

* Document naming conventions
* Define standard response formats
* Specify error handling practices
* Set expectations for documentation

### 12.3 Developer Experience

* Provide **client libraries** in major languages
* Maintain comprehensive **API documentation**
* Create **quickstart guides** and **tutorials**
* Gather and act on **developer feedback**

---

## 13. GraphQL API Guidelines

### 13.1 Schema Design

* Design schemas around **domain models**
* Use **descriptive names** for types and fields
* Include **descriptions** for all schema elements
* Implement **interfaces** for shared fields

```graphql
"""
A user in the system
"""
type User {
  """
  Unique identifier for the user
  """
  id: ID!

  """
  Username for login
  """
  username: String!

  """
  Email address
  """
  email: String!

  """
  User's full name
  """
  fullName: String

  """
  User's profile image
  """
  profileImage: Image

  """
  List of content items created by this user
  """
  contentItems(
    """Limit the number of items returned"""
    limit: Int = 10,

    """Skip the specified number of items"""
    offset: Int = 0,

    """Filter by status"""
    status: ContentStatus
  ): [ContentItem!]!
}

"""
Status of a content item
"""
enum ContentStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

"""
Interface for media items
"""
interface Media {
  id: ID!
  url: String!
  mimeType: String!
  width: Int
  height: Int
}

"""
An image in the system
"""
type Image implements Media {
  id: ID!
  url: String!
  mimeType: String!
  width: Int
  height: Int
  altText: String
  caption: String
}
```

### 13.2 Query Design

* Support **field selection** to avoid over-fetching
* Implement **pagination** for lists
* Use **arguments** for filtering and sorting
* Return **partial results** with errors when possible

```graphql
# Example query with field selection, filtering, and pagination
query GetUserContentItems {
  user(id: "123") {
    id
    username
    contentItems(
      status: PUBLISHED,
      limit: 5,
      offset: 0,
      sortBy: CREATED_AT,
      sortDirection: DESC
    ) {
      id
      title
      summary
      createdAt
      # Only fetch author details we need
      author {
        id
        username
      }
      # Only fetch image details we need
      featuredImage {
        url
        width
        height
      }
    }
  }
}
```

### 13.3 Mutations

* Name mutations with **verb-noun** convention
* Return the **modified resource** in response
* Include **input validation** errors
* Support **optimistic UI updates**

```graphql
# Example mutation
mutation UpdateUserProfile($input: UpdateUserProfileInput!) {
  updateUserProfile(input: $input) {
    # Return the updated user
    user {
      id
      username
      fullName
      bio
      preferences {
        theme
        emailNotifications
      }
    }
    # Return any validation errors
    errors {
      field
      message
    }
  }
}

# Input type for the mutation
input UpdateUserProfileInput {
  id: ID!
  fullName: String
  bio: String
  preferences: UserPreferencesInput
}

input UserPreferencesInput {
  theme: Theme
  emailNotifications: Boolean
}

enum Theme {
  LIGHT
  DARK
  SYSTEM
}
```

---

## 14. WebSocket API Guidelines

### 14.1 Connection Management

* Implement **authentication** for WebSocket connections
* Handle connection **timeouts** and **disconnects**
* Support **reconnection** with state recovery
* Limit **connection count** per client

```javascript
// Example WebSocket server in Node.js with Socket.io
const app = require('express')();
const http = require('http').createServer(app);
const io = require('socket.io')(http, {
  cors: {
    origin: "https://app.thinkalike.com",
    methods: ["GET", "POST"],
    credentials: true
  }
});
const jwt = require('jsonwebtoken');

// Connection middleware for authentication
io.use((socket, next) => {
  // Get token from handshake auth
  const token = socket.handshake.auth.token;
  if (!token) {
    return next(new Error("Authentication error"));
  }

  try {
    // Verify JWT token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    socket.user = decoded;
    next();
  } catch (err) {
    return next(new Error("Authentication error"));
  }
});

// Connection event
io.on('connection', (socket) => {
  console.log(`User connected: ${socket.user.id}`);

  // Add user to appropriate rooms
  socket.join(`user:${socket.user.id}`);

  // Example: Join user to their team rooms
  getUserTeams(socket.user.id).then(teams => {
    teams.forEach(team => {
      socket.join(`team:${team.id}`);
    });
  });

  // Handle disconnection
  socket.on('disconnect', () => {
    console.log(`User disconnected: ${socket.user.id}`);
    // Clean up any user-specific resources
  });

  // Example event handler
  socket.on('subscribe:topic', (topic) => {
    // Validate topic format
    if (!/^[a-z0-9-]+$/.test(topic)) {
      socket.emit('error', {
        code: 'invalid_topic',
        message: 'Invalid topic format'
      });
      return;
    }

    // Check if user has permission to subscribe
    canSubscribeToTopic(socket.user.id, topic).then(canSubscribe => {
      if (canSubscribe) {
        socket.join(`topic:${topic}`);
        socket.emit('subscribed', { topic });
      } else {
        socket.emit('error', {
          code: 'permission_denied',
          message: 'You do not have permission to subscribe to this topic'
        });
      }
    });
  });
});

// Function to limit connections per user
function limitConnectionsPerUser(userId, maxConnections = 5) {
  const userSockets = getUserSockets(userId);

  if (userSockets.length >= maxConnections) {
    // Disconnect oldest connection
    const oldestSocket = userSockets[0];
    oldestSocket.emit('force_disconnect', {
      reason: 'too_many_connections',
      message: 'Too many open connections'
    });
    oldestSocket.disconnect(true);
  }
}
```

### 14.2 Message Format

* Use a **consistent message format**
* Include **message type** for routing
* Add **correlation IDs** for request-response pairs
* Include **timestamps** for ordering

```javascript
// Example message format
const messageTypes = {
  // Server -> Client
  SERVER_EVENT: 'server:event',
  SERVER_RESPONSE: 'server:response',
  SERVER_ERROR: 'server:error',

  // Client -> Server
  CLIENT_REQUEST: 'client:request',
  CLIENT_ACTION: 'client:action'
};

// Example client request
const clientRequest = {
  type: messageTypes.CLIENT_REQUEST,
  id: '123e4567-e89b-12d3-a456-426614174000', // UUID for correlation
  timestamp: new Date().toISOString(),
  resource: 'messages',
  action: 'get',
  payload: {
    channelId: '456',
    limit: 50,
    before: '2023-05-01T12:00:00Z'
  }
};

// Example server response
const serverResponse = {
  type: messageTypes.SERVER_RESPONSE,
  id: '789e4567-e89b-12d3-a456-426614174111', // New UUID for this message
  correlationId: '123e4567-e89b-12d3-a456-426614174000', // Matches client request
  timestamp: new Date().toISOString(),
  resource: 'messages',
  action: 'get',
  status: 'success',
  payload: {
    messages: [/* array of message objects */],
    pagination: {
      hasMore: true,
      nextCursor: '2023-04-30T18:30:00Z'
    }
  }
};

// Example server error response
const serverError = {
  type: messageTypes.SERVER_ERROR,
  id: '999e4567-e89b-12d3-a456-426614174222',
  correlationId: '123e4567-e89b-12d3-a456-426614174000', // Matches client request
  timestamp: new Date().toISOString(),
  resource: 'messages',
  action: 'get',
  status: 'error',
  error: {
    code: 'permission_denied',
    message: 'You do not have permission to access this channel',
    details: {
      channelId: '456',
      requiredRole: 'member'
    }
  }
};

// Example server event (push notification)
const serverEvent = {
  type: messageTypes.SERVER_EVENT,
  id: '444e4567-e89b-12d3-a456-426614174333',
  timestamp: new Date().toISOString(),
  event: 'message:created',
  payload: {
    message: {
      id: '789',
      channelId: '456',
      userId: '123',
      content: 'Hello world',
      createdAt: '2023-05-01T12:30:00Z'
    }
  }
};
```

### 14.3 Event Broadcasting

* Use **channels** or **rooms** for topic-based messaging
* Implement **authorization** for publishing events
* Support **filtering** of events on the server side
* Provide **presence** information when appropriate

```javascript
// Example broadcasting to different scopes
function broadcastMessage(message) {
  const { channelId, teamId, isPublic } = message;

  // Send to specific channel
  io.to(`channel:${channelId}`).emit('message:new', formatMessage(message));

  // Send to team for activity feeds
  io.to(`team:${teamId}`).emit('activity:new', formatActivity(message));

  // If public, broadcast to site visitors
  if (isPublic) {
    io.to('public').emit('public:activity', formatPublicActivity(message));
  }
}

// Handle presence updates
function updatePresence(userId, status) {
  // Get user data
  const user = getUserData(userId);

  // Broadcast to all relevant teams
  user.teams.forEach(team => {
    io.to(`team:${team.id}`).emit('presence:update', {
      userId,
      status,
      lastSeen: new Date().toISOString()
    });
  });

  // Store presence info in Redis for new connections
  storePresenceInfo(userId, status);
}

// Get initial presence info for a team
function getTeamPresence(teamId) {
  return getTeamMembers(teamId)
    .then(members => {
      return Promise.all(
        members.map(member => getPresenceInfo(member.id))
      );
    });
}

// Example usage in connection handler
socket.on('connection', (socket) => {
  // ...

  socket.on('presence:update', (status) => {
    updatePresence(socket.user.id, status);
  });

  socket.on('presence:get', ({ teamId }) => {
    // Check permissions
    if (isTeamMember(socket.user.id, teamId)) {
      getTeamPresence(teamId).then(presence => {
        socket.emit('presence:list', { teamId, presence });
      });
    } else {
      socket.emit('error', {
        code: 'permission_denied',
        message: 'Not a team member'
      });
    }
  });
});
```

---

By following these backend API development guidelines, ThinkAlike ensures consistency, reliability, and security across all APIs, making integration easier for clients while maintaining a robust and maintainable system.
