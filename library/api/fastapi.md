# Skill: FastAPI Python Backend

## Overview
Build a REST API with FastAPI - fast, async, auto-documented Python backend.

## Tech Stack
- Language: Python 3.11+
- Framework: FastAPI
- ORM: SQLAlchemy 2.0 (async)
- Database: PostgreSQL (default) or SQLite (dev)
- Auth: JWT with python-jose
- Validation: Pydantic v2
- Server: Uvicorn

## Project Structure
```
project/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/   # Route handlers
│   │   │   └── router.py
│   ├── core/
│   │   ├── config.py        # Settings
│   │   ├── security.py      # Auth helpers
│   │   └── deps.py          # Dependencies
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── db/
│   │   └── session.py       # DB connection
│   └── main.py
├── tests/
├── alembic/                 # DB migrations
├── .env
├── requirements.txt
└── docker-compose.yml
```

## Setup Steps
1. `pip install fastapi uvicorn[standard] sqlalchemy pydantic-settings`
2. Create `app/main.py` with FastAPI instance
3. Set up `app/core/config.py` with Pydantic settings
4. Configure database in `app/db/session.py`
5. Create models, schemas, and endpoints

## Conventions & Patterns
- Separate Pydantic schemas from SQLAlchemy models
- Use dependency injection for DB sessions and auth
- Return Pydantic schemas, not raw models
- Group routes by feature/resource in `api/v1/endpoints/`
- Use `async def` for all route handlers

## Common Commands
```bash
uvicorn app.main:app --reload    # Dev server
alembic init alembic             # Init migrations
alembic revision --autogenerate  # Generate migration
alembic upgrade head             # Apply migrations
pytest tests/                    # Run tests
```

## Best Practices
- Always validate input with Pydantic schemas
- Use `Depends()` for dependency injection
- Set CORS middleware for frontend access
- Use `.env` files + Pydantic Settings for config
- Add response_model to all endpoints
- Use HTTPException for all errors

## Common Pitfalls
- Don't use sync SQLAlchemy with async FastAPI
- Don't put business logic in route handlers - use services
- Don't forget to close DB sessions (use context managers)
- Remember to add CORS origins for frontend

## Example main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router, prefix="/api/v1")
```

## References
- Docs: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
