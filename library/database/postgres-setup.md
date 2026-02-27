# Skill: PostgreSQL Database Setup

## Overview
Set up and configure a PostgreSQL database for a project, including schema design, migrations, and connection setup.

## Tech Stack
- Database: PostgreSQL 16+
- Migrations: Alembic (Python) or Flyway / Prisma (Node)
- ORM: SQLAlchemy (Python) or Prisma / Drizzle (Node)
- Dev Tool: Docker Compose for local dev

## Docker Compose Setup (Quick Start)
```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Connection String Format
```
postgresql://user:password@localhost:5432/mydb
# Async:
postgresql+asyncpg://user:password@localhost:5432/mydb
```

## SQLAlchemy Models Pattern (Python)
```python
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
```

## Conventions
- Always use UUIDs or auto-increment integer PKs
- Add `created_at` and `updated_at` to every table
- Use snake_case for table and column names
- Add indexes on foreign keys and frequently queried columns
- Never store passwords in plain text (use bcrypt)

## Common Commands
```bash
# Docker
docker-compose up -d db           # Start DB
docker-compose exec db psql -U user -d mydb  # Connect

# Alembic
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1

# Prisma
npx prisma init
npx prisma generate
npx prisma migrate dev
```

## Best Practices
- Use connection pooling (asyncpg, pgbouncer)
- Set `pool_pre_ping=True` to handle stale connections
- Use transactions for multi-step operations
- Add `NOT NULL` constraints where data is required
- Back up production DBs before migrations

## Common Pitfalls
- Don't run migrations in production without testing on staging first
- Don't use `text` for columns with known max lengths
- Don't forget to index foreign key columns
- Avoid N+1 queries - use eager loading

## References
- PostgreSQL: https://www.postgresql.org/docs/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Prisma: https://www.prisma.io/docs/
