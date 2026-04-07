Micro Service Framework Sandbox
===============================

This repository contains a minimal example stack:

- Nginx reverse proxy (public endpoint)
- FastAPI `gateway` service (JWT validation / API forwarding)
- FastAPI `customer` service (CRUD over PostgreSQL via SQLAlchemy + psycopg)
- React SPA (Vite) frontend


