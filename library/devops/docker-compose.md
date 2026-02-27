# Skill: Docker + Docker Compose

## Overview
Containerize applications and set up multi-service development and production environments.

## Core Concepts
- **Dockerfile** - Recipe to build an image
- **docker-compose.yml** - Define and run multi-container apps
- **.dockerignore** - Files to exclude from build context

## Python App Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Node App Dockerfile
```dockerfile
FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Full Stack docker-compose.yml
```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy

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
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## .dockerignore
```
node_modules/
__pycache__/
*.pyc
.env
.git/
dist/
*.log
```

## Common Commands
```bash
docker-compose up -d              # Start all services
docker-compose down               # Stop all services
docker-compose down -v            # Stop and remove volumes
docker-compose logs -f service    # Follow logs
docker-compose exec service bash  # Shell into container
docker-compose build --no-cache   # Rebuild images
docker ps                         # List running containers
docker images                     # List images
```

## Best Practices
- Use `depends_on` with `condition: service_healthy`
- Never put secrets in Dockerfile - use env files or secrets
- Use multi-stage builds to reduce image size
- Pin image versions (not `latest`) in production
- Use `.env` file for docker-compose variables

## Common Pitfalls
- `localhost` inside a container = the container itself, not host
- Use service name (e.g., `db`) to communicate between containers
- Don't run as root in containers (add USER directive)
- Volume mounts override container files

## References
- Docker: https://docs.docker.com/
- Compose: https://docs.docker.com/compose/
