# Building a Backend API Endpoint

This guide details the process for creating new API endpoints within the ThinkAlike FastAPI backend. It covers routing, request/response modeling, service layer interaction, database access, testing, and integration with the Verification System.

**Prerequisites:**

* Familiarity with Python 3.10+, FastAPI, Pydantic, SQLAlchemy, and RESTful API principles.

* Understanding of the project's [Code Style Guide](./code_style_guide.md) (Backend section).

* Familiarity with the [Architectural Overview](../architecture/architectural_overview.md) and the role of the Verification System (see [Verification System Deep Dive](../architecture/verification_system/verification_system_deep_dive.md)).

* A local backend environment set up as per the [Installation Guide](../core/installation.md).

---

## 1. Planning & Design

* **Define the Endpoint:**

  * Determine the purpose, HTTP method (GET, POST, PUT, DELETE, etc.), and URL path following RESTful conventions.

* **Define the Request:**

  * Specify path parameters, query parameters, and the request body structure.

  * Use Pydantic models to validate request bodies.

* **Define the Response:**

  * Specify success response status codes (e.g., 200, 201, 204) and body structures using Pydantic models.

  * Define error responses (e.g., 400, 401, 403, 404, 500) and their potential body structures.

* **Service Logic:**

  * Identify the business logic that must be executed; this should reside within the service layer.

* **Data Access:**

  * Identify data interactions (both read/write) with the database.

* **Verification Needs:**

  * Determine if and when the operation should trigger ethical and functional validations via the Verification System.

* **Permissions:**

  * Define the required authentication/authorization level (e.g., authenticated user, specific role).

* **Documentation:**

  * Update or add the new endpoint definition in the relevant API documentation file (e.g., `docs/architecture/api/api_endpoints_modeX.md`).

---

## 2. Implementation Steps

### 2.1. Define Models (Pydantic)

In the designated area (e.g., `backend/models/schemas/`), define the Pydantic models for your request and response.

```python

# Example: backend/models/schemas/profile_schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProfileUpdate(BaseModel):
    display_name: Optional[str] = Field(None, min_length=3, max_length=50)
    interests: Optional[List[str]] = None

class ProfileResponse(BaseModel):
    user_id: int
    display_name: str
    interests: List[str]
    last_updated: datetime

    class Config:
        orm_mode = True  # To allow conversion from SQLAlchemy models

```

## 2.2. Create/Update Router

### 2.2. Create/Update Router

Locate the appropriate `APIRouter` file (e.g., in `backend/routes/user_routes.py`) or create a new one if needed.

* Define the endpoint function using the correct FastAPI decorator.

* Use type hints for path/query parameters and the request body.

* Leverage FastAPI’s dependency injection (`Depends`) for database sessions and service layers.

* Implement authentication/authorization checks with FastAPI dependencies.

```python

# Example: backend/routes/user_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, models, services
from ..dependencies import get_db, get_current_active_user  # Assuming these exist

from ..models.schemas import profile_schemas

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],  # Apply auth to all routes here

    responses={404: {"description": "Not found"}},
)

@router.put(
    "/{user_id}/profile",
    response_model=profile_schemas.ProfileResponse,
    summary="Update User Profile"
)
async def update_user_profile(
    user_id: int,
    profile_data: profile_schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
    profile_service: services.ProfileService = Depends(services.ProfileService)  # Inject service

):
    # Authorization check: Ensure user can only update their own profile (or admin)

    if user_id != current_user.id and not current_user.is_superuser:
         raise HTTPException(
             status_code=status.HTTP_403_FORBIDDEN,
             detail="Not authorized to update this profile",
         )

    # Call the service layer to handle the logic

    updated_profile = await profile_service.update_profile(
        db=db, user_id=user_id, profile_update_data=profile_data
    )
    if updated_profile is None:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_profile

```

## 2.3. Implement Service Logic

### 2.3. Implement Service Logic

In the service layer (e.g., `backend/services/profile_service.py`), encapsulate the business logic for your endpoint.

* Accept necessary parameters such as the DB session, user ID, and input data.

* Integrate a Verification Hook: Call the Verification System’s API/interface at the appropriate junction.

* Interact with the database using CRUD functions or direct SQLAlchemy operations.

* Return results or raise exceptions as needed.

```python

# Example: backend/services/profile_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import crud, models
from ..models.schemas import profile_schemas
from .verification_service import VerificationService  # Assuming a service to interact with Verification System

class ProfileService:
    def __init__(self, verification_service: VerificationService = VerificationService()):
        self.verification_service = verification_service

    async def update_profile(self, db: Session, user_id: int, profile_update_data: profile_schemas.ProfileUpdate) -> models.User | None:
        db_user = crud.user.get(db, id=user_id)
        if not db_user:
            return None

        update_data = profile_update_data.dict(exclude_unset=True)

        # Verification Hook Example (Pre-Update)

        if 'display_name' in update_data:
             is_valid, reason = await self.verification_service.verify_action(
                 action="update_display_name",
                 context={"user_id": user_id, "new_name": update_data['display_name']}
             )
             if not is_valid:
                 raise HTTPException(
                     status_code=status.HTTP_400_BAD_REQUEST,
                     detail=f"Display name validation failed: {reason}"
                 )

        # Update user data using CRUD operations

        updated_user = crud.user.update(db=db, db_obj=db_user, obj_in=update_data)
        return updated_user

```

## 2.4. Add CRUD Operations (if necessary)

### 2.4. Add CRUD Operations (if necessary)

If new database interactions are required, add reusable CRUD functions (e.g., in `backend/crud/crud_user.py`). These should handle basic SQLAlchemy operations such as get, create, update, and delete.

### 2.5. Register the Router

Ensure your new or updated router is included in the main FastAPI application. In `backend/main.py`, add:

```python
from fastapi import FastAPI
from backend.routes import user_routes

app = FastAPI()
app.include_router(user_routes.router)

```

---

## 3. Testing

### Unit Testing (Services)

* Write tests for your service methods in isolation.

* Mock the database session, CRUD functions, and the Verification System calls.

* Ensure your validations and data transformations are correct.

### Integration Testing (Endpoints)

* Use FastAPI’s `TestClient` to send requests to your endpoints.

* Verify status codes, response bodies, and database state changes.

* Test authentication/authorization enforcement.

* Optionally, mock Verification System calls if they are complex or external.

```python

# Example Integration Test Snippet (backend/tests/api/v1/test_users.py)

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .... import models
from ....models.schemas.profile_schemas import ProfileResponse

def test_update_own_profile(client: TestClient, db: Session, normal_user_token_headers: dict, normal_user: models.User) -> None:
    update_data = {"display_name": "Updated Name Test"}
    response = client.put(
        f"/api/v1/users/{normal_user.id}/profile",  # Adjust prefix as needed

        headers=normal_user_token_headers,
        json=update_data,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "Updated Name Test"
    assert data["user_id"] == normal_user.id

    # Verify DB change

    db.refresh(normal_user)
    assert normal_user.display_name == "Updated Name Test"

def test_update_other_user_profile_forbidden(client: TestClient, db: Session, normal_user_token_headers: dict) -> None:
    # Assuming another user with ID 999 exists

    update_data = {"display_name": "Forbidden Update"}
    response = client.put(
        f"/api/v1/users/999/profile",  # Adjust prefix as needed

        headers=normal_user_token_headers,
        json=update_data,
    )
    assert response.status_code == 403  # Or 401 depending on auth setup

```

---

## 4. Manual Testing

* Run the backend server locally.

* Use tools like curl, Postman, or the Swagger UI (accessible at `/docs`) to manually test the endpoint.

* Integrate with the frontend and perform end-to-end testing.

* Test various valid and invalid inputs to ensure endpoint robustness.

---

By following this structured approach—covering design, implementation, tests, and manual verification—you ensure new backend endpoints are robust, secure, and fully aligned with ThinkAlike’s core principles.

---

**Document Details**

* Title: Building a Backend Api Endpoint

* Type: Developer Guide

* Version: 1.0.0

* Last Updated: 2025-04-05

---

End of Building a Backend Api Endpoint

---
