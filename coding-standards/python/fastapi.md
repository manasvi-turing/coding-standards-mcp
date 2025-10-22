---
description: Fast API coding standards and best practices
status: active
---

# FastAPI Coding Standards

## 1. Objective
Establish a **consistent, readable, and scalable** coding framework for FastAPI projects based on a **top-down design** and **builder-style initialization** pattern.

This ensures that:
- The application’s **structure is clear from entrypoint downward**.
- Business logic and routes are **modular and easily testable**.
- **Dependencies, middleware, and routes** are loaded declaratively and predictably.

---

## 2. Architectural Mind Map

**Top-Down Flow**
```

main.py (entrypoint)
└── ApplicationBuilder
├── add_config()
├── add_routes()
├── add_middleware()
├── add_dependencies()
└── build()
├── FastAPI(app)
├── Routers registered
├── Middleware applied
└── App returned

````

**Code Layers**
- `main.py` → Application initialization (top-level builder).
- `app/routers/` → Route definitions (REST endpoints, grouped by domain).
- `app/services/` → Business logic and controllers.
- `app/models/` → Pydantic models (Request/Response schemas).
- `app/core/` → Configs, middleware, dependency injection, settings.
- `app/utils/` → Shared utility functions (e.g., logger, validators).

---

## 3. Folder Structure Standard

```plaintext
project-root/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   └── middleware.py
│   │
│   ├── routers/
│   │   ├── user_router.py
│   │   ├── auth_router.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   └── auth_service.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── auth.py
│   │
│   ├── utils/
│   │   └── logger.py
│   │
│   └── builder.py
│
└── main.py
````

---

## 4. Top-Down Application Pattern

### 4.1 main.py

```python
from app.builder import ApplicationBuilder

def create_app():
    app = (
        ApplicationBuilder()
        .add_config()
        .add_routes()
        .add_middleware()
        .add_dependencies()
        .build()
    )
    return app

app = create_app()
```

---

### 4.2 builder.py

```python
from fastapi import FastAPI
from app.routers import user_router, auth_router
from app.core.middleware import register_middlewares
from app.core.dependencies import register_dependencies
from app.core.config import settings

class ApplicationBuilder:
    def __init__(self):
        self.app = None

    def add_config(self):
        self.app = FastAPI(
            title=settings.PROJECT_NAME,
            version=settings.VERSION,
            docs_url="/docs",
            redoc_url="/redoc"
        )
        return self

    def add_routes(self):
        self.app.include_router(user_router.router, prefix="/users", tags=["Users"])
        self.app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
        return self

    def add_middleware(self):
        register_middlewares(self.app)
        return self

    def add_dependencies(self):
        register_dependencies(self.app)
        return self

    def build(self):
        return self.app
```

---

## 5. Route Definition Standard

Each route file must:

* Contain a `router` object.
* Group related endpoints logically.
* Keep routes small (<= 100 lines recommended).
* Delegate logic to service layer.

```python
# app/routers/user_router.py
from fastapi import APIRouter, Depends
from app.models.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(payload: UserCreate, service: UserService = Depends()):
    return await service.create_user(payload)
```

---

## 6. Service Layer Convention

* Encapsulate business logic.
* Avoid direct DB or API access from routers.
* Use dependency injection for external resources (DB, cache, etc.).

```python
# app/services/user_service.py
from app.models.user import UserCreate, UserResponse

class UserService:
    async def create_user(self, payload: UserCreate) -> UserResponse:
        # Example logic
        user = {"id": 1, "name": payload.name}
        return UserResponse(**user)
```

---

## 7. Configuration & Environment

Centralize configuration under `app/core/config.py`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Service"
    VERSION: str = "1.0.0"
    ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
```

Use `settings` throughout for consistency.

---

## 8. Middleware & Dependencies

### Middleware Registration

```python
# app/core/middleware.py
from fastapi.middleware.cors import CORSMiddleware

def register_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
```

### Dependency Injection Setup

```python
# app/core/dependencies.py
def register_dependencies(app):
    @app.on_event("startup")
    async def startup_event():
        # e.g., connect to DB
        pass

    @app.on_event("shutdown")
    async def shutdown_event():
        # e.g., close connections
        pass
```

---

## 9. Logging Standard

Use a **central logger utility**:

```python
# app/utils/logger.py
import logging

def get_logger(name="app"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
```

Usage:

```python
from app.utils.logger import get_logger
logger = get_logger(__name__)
logger.info("User service initialized")
```

---

## 10. Testing & Maintainability

* Use **pytest** for unit and integration tests.
* Each router and service should have corresponding tests under `/tests`.
* Test the **builder initialization** to ensure routes and middlewares load properly.

Example:

```bash
pytest -v --disable-warnings
```

---

## 11. Key Coding Practices

| Principle                  | Rule                                                                   |
| -------------------------- | ---------------------------------------------------------------------- |
| **Top-Down Readability**   | The main file (`main.py`) must fully describe the system’s setup path. |
| **Builder Pattern**        | All app setup actions chained in a single builder.                     |
| **Separation of Concerns** | Routes → Services → Models → Configs.                                  |
| **Declarative Configs**    | No hard-coded values in routers/services.                              |
| **Dependency Injection**   | All external systems must be injected, not imported directly.          |
| **Extensibility**          | Adding new routes or middleware should require minimal code change.    |

---

## 12. Future Enhancements

* Add **dynamic module auto-discovery** for routers and middleware.
* Add **health-check endpoint** via builder (`.add_healthcheck()`).
* Integrate **structured logging** (JSON) for observability.
* Allow `.add_plugins()` extension point for optional modules (cache, auth, etc.).
* Generate **OpenAPI summary dashboard** at `/meta/docs`.

---

## 13. Summary

* **Top-down entrypoint (`main.py`) defines entire app flow.**
* **Builder encapsulates construction steps** for easy readability.
* **Routes, services, configs, and middlewares** are modular and discoverable.
* **Consistency and clarity** take priority over brevity.
* This pattern supports **scalability, testing, and AI-assisted orchestration** later.

---

