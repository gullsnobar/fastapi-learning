# FastAPI Patient Management API

A small FastAPI application for creating, reading, filtering, sorting, and deleting patient records. It uses Pydantic for validation and a local JSON file for storage.

## Project structure

```text
.
|-- app/
|   |-- __init__.py
|   |-- database.py      # JSON-backed patient repository
|   |-- main.py          # Application factory and FastAPI instance
|   |-- models.py        # Request models and validation
|   `-- routes.py        # HTTP endpoints
|-- data/
|   `-- patients.json    # Local development data
|-- tests/
|   `-- test_api.py      # API behavior tests
|-- .python-version
|-- pyproject.toml
`-- uv.lock
```

This layout keeps application code, mutable data, and tests separate without adding layers the project does not need yet.

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)

## Setup and run

Install the locked dependencies:

```bash
uv sync
```

Start the development server:

```bash
uv run fastapi dev app/main.py
```

The API is available at `http://127.0.0.1:8000`. Interactive documentation is available at `/docs`, with ReDoc at `/redoc`.

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | API welcome message |
| `GET` | `/about` | API description |
| `GET` | `/view` | List, filter, or sort patients |
| `GET` | `/patient/{patient_id}` | Get one patient |
| `POST` | `/create` | Create a patient |
| `DELETE` | `/delete/{patient_id}` | Delete a patient |

### List and filter patients

`GET /view` accepts these optional query parameters:

- `city`: case-insensitive city filter
- `sort_by`: `age`, `weight`, or `bmi`
- `order`: `asc` (default) or `desc`

Examples:

```text
GET /view?city=Karachi
GET /view?sort_by=age&order=desc
```

### Create a patient

```http
POST /create
Content-Type: application/json
```

```json
{
  "name": "Alex Morgan",
  "email": "alex.morgan@example.com",
  "age": 32,
  "gender": "Male",
  "weight": 72.5,
  "height": 1.78,
  "married": false,
  "allergies": ["Peanuts"],
  "address": {
    "city": "Karachi",
    "state": "Sindh",
    "pin_code": "74000"
  }
}
```

BMI is calculated automatically. Email addresses must be unique among records that include an email.

## Tests

Run the test suite without additional test dependencies:

```bash
uv run python -m unittest discover -s tests -v
```

## Storage note

`data/patients.json` is suitable for learning and local development. A production service should use a transactional database and handle concurrent writes explicitly.
