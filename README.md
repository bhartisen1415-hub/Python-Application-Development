# Python Application Development API

A REST API built with FastAPI, SQLite, and Pydantic.

## Features

- FastAPI routing and HTTP methods (GET, POST, PUT, DELETE)
- SQLite database integration
- Create, Read, Update, and Delete (CRUD)
- API key authentication (`X-API-Key` header)
- Request validation with Pydantic
- Automated API tests
- Interactive API docs (Swagger UI)

## Requirements

- Python 3.10 or later

## Installation

    python -m venv .venv

Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

Install dependencies:

    python -m pip install -r requirements.txt

## Run the API

    python -m uvicorn app.main:app --reload

Open http://127.0.0.1:8000/docs and click **Authorize** to enter the API key.

## Authentication

Protected endpoints need the `X-API-Key` header. Default key for local learning:

    dev-secret-change-me

Set the `API_KEY` environment variable before any real deployment (see `.env.example`).

## Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | API information |
| GET | /health | Health check |
| POST | /items | Create an item |
| GET | /items | List all items |
| GET | /items/{item_id} | Get one item |
| PUT | /items/{item_id} | Update an item |
| DELETE | /items/{item_id} | Delete an item |

## Run tests

The server does not need to be running.

    python -m unittest discover -s tests -v

## Database

`items.db` is created automatically when the app starts.
