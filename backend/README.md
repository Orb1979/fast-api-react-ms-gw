Backend Mono-Repo
=================

This directory contains all backend services and infrastructure:

- `gateway/` – FastAPI JWT-validating gateway / reverse proxy
- `customer/` – FastAPI CRUD API (PostgreSQL + SQLAlchemy + psycopg)
- `nginx/` – Nginx reverse proxy config + Dockerfile
- `docker-compose.yml` – Local stack: Postgres and optional proxy/services

Services
--------

- **Gateway-service (FastAPI)**
  - Validates JWTs issued by Auth0 and forwards `/api/{service}/**` requests to downstream services.

- **Customer-service (FastAPI)**
  - Simple CRUD REST API backed by PostgreSQL using SQLAlchemy ORM and psycopg.

Docker Compose
--------------
- `docker-compose.yml` - postgresSql  
- `docker-compose-dev-nginx.yml` - postgresSql + nginx (nginx forwards directly to microservice)
- `docker-compose-dev-nginx-gw.yml` - postgresSql + nginx (nginx forwards through gateway service)
- `docker-compose-stg.yml` -postgresSql + nginx container + microservices


During local development you can:
- Run FastAPI apps directly from your IDE or with `uvicorn`
- Run the DB + nginx via `docker compose up -d`
- Hit the services either:
  - Directly (`http://localhost:8080`, `http://localhost:8081`), or
  - Via nginx (`http://localhost/` and `/api/**`)

Local Python config (no shell exports needed)
---------------------------------------------
Both FastAPI services ship with sensible defaults in code, so local runs work without `export ...`.

- Customer defaults:
  - `DATABASE_URL=postgresql+psycopg://msf_user:msf_password@localhost:5432/msf_customer`
- Gateway defaults:
  - `ISSUER_URI=https://dev-lc6vtcbv5ll7xa31.eu.auth0.com/`
  - `AUDIENCE=https://dev-lc6vtcbv5ll7xa31.eu.auth0.com/api/v2/`
  - `CUSTOMER_SERVICE_URL=http://localhost:8081/api/customer`

You can still override per service by creating a local `.env` file (ignored by git):

- `customer/.env` (optional, see `customer/.env.example`)
- `gateway/.env` (optional, see `gateway/.env.example`)

Database migrations (Alembic)
-----------------------------
Customer service uses Alembic for versioned PostgreSQL migrations.

- Apply latest migrations:
  - `cd customer && alembic upgrade head`
- Create a new migration revision:
  - `cd customer && alembic revision -m "your_message"`

