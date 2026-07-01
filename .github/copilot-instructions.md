# Copilot Instructions for Mergington High School Activities API

## Project Overview

This is a **Python/FastAPI** web application called the **Mergington High School Management System**. It allows students to view and sign up for extracurricular activities. The app exposes a REST API backed by an in-memory data store, and serves a simple HTML/CSS/JS frontend from the `src/static/` directory.

## Repository Structure

```
.
├── src/
│   ├── app.py              # FastAPI application — all API routes and in-memory data
│   └── static/
│       ├── index.html      # Single-page frontend
│       ├── app.js          # Frontend JS (fetches API, handles signup/unregister)
│       └── styles.css      # Frontend styling
├── tests/
│   ├── conftest.py         # pytest fixtures (TestClient, activity snapshot/restore)
│   └── test_app.py         # API integration tests
├── requirements.txt        # Python dependencies (fastapi, uvicorn, httpx, watchfiles, pytest)
├── pytest.ini              # pytest config: pythonpath = .
└── .devcontainer/
    └── devcontainer.json   # Python 3.13 devcontainer, forwardPorts: [8000]
```

## Technology Stack

- **Backend:** Python 3.13, FastAPI, Uvicorn
- **Frontend:** Vanilla HTML/CSS/JavaScript (no build step required)
- **Testing:** pytest with FastAPI's `TestClient` (via httpx)
- **Data storage:** In-memory Python dict (no database — data resets on restart)

## Development Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the development server (from the `src/` directory):
```bash
uvicorn app:app --reload
```

Or from the repo root:
```bash
uvicorn src.app:app --reload
```

The app serves at `http://localhost:8000`. The root `/` redirects to `/static/index.html`.
FastAPI auto-docs are available at `/docs` and `/redoc`.

## Running Tests

From the repository root (required — `pytest.ini` sets `pythonpath = .`):
```bash
pytest
```

Tests use an `autouse` fixture (`restore_activities`) that snapshots and restores the in-memory `activities` dict after each test, so tests are fully isolated. No external services or databases are needed.

## API Endpoints

| Method   | Endpoint                                              | Description                        |
|----------|-------------------------------------------------------|------------------------------------|
| GET      | `/`                                                   | Redirects to `/static/index.html`  |
| GET      | `/activities`                                         | List all activities with details   |
| POST     | `/activities/{activity_name}/signup?email=<email>`    | Sign a student up for an activity  |
| DELETE   | `/activities/{activity_name}/participants/{email}`    | Unregister a student from activity |

## Data Model

All data lives in `src/app.py` as a module-level dict named `activities`. Each activity has:
- `description` (str)
- `schedule` (str)
- `max_participants` (int)
- `participants` (list of email strings)

Students are identified solely by email address. There is no persistent database.

## Key Conventions

- **No database migrations** — all data is in-memory; changes to the data model mean editing the `activities` dict directly in `app.py`.
- **Email as student identifier** — student emails are stored as plain strings in `participants` lists.
- **Error handling** — use FastAPI `HTTPException` with appropriate HTTP status codes (404 for missing activity/participant, 400 for duplicates).
- **Test isolation** — tests rely on the `restore_activities` autouse fixture in `conftest.py`; never mutate module-level state without accounting for this.
- **Static files** — the frontend is plain HTML/JS/CSS in `src/static/`; no npm, no bundler, no build step.
- **pythonpath** — `pytest.ini` adds `.` to the Python path, so imports use `src.app` (e.g., `import src.app as app_module`).

## Common Tasks

- **Add a new activity:** Add an entry to the `activities` dict in `src/app.py`.
- **Add a new API endpoint:** Add a route function to `src/app.py` using FastAPI decorators.
- **Add a new test:** Add to `tests/test_app.py`; use the `client` fixture from `conftest.py`.
- **Update the frontend UI:** Edit files in `src/static/` (no build step needed).

## Known Errors & Workarounds

- **Running the server from `src/`:** If you `cd src && uvicorn app:app --reload`, the static files mount path resolves correctly. From the repo root, use `uvicorn src.app:app --reload` and ensure the working directory contains `src/`.
- **pytest must run from repo root:** Because `pytest.ini` sets `pythonpath = .`, running `pytest` from inside `src/` or `tests/` will cause import errors (`ModuleNotFoundError: No module named 'src'`). Always run `pytest` from the repository root.
- **In-memory data resets on restart:** This is by design. Do not rely on activity data persisting across server restarts during development.
