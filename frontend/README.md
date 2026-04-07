Frontend SPA (Vite + React)
===========================

This directory contains the React single-page application built with Vite.

Development
-----------

```bash
cd frontend/
npm install
npm run dev
```
npm install @auth0/auth0-react
npm install jwt-decode


The app runs on `http://localhost:5173`.
It calls the Customer API at `/api/customer` 

Production Build
----------------

```bash
cd frontend/
npm run build
```

The static files will be generated in `dist/`. You can:

- Serve them with `npm run preview`, or
- Copy them into the nginx image under `/usr/share/nginx/html` for a production-like setup.

