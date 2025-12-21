# Rio Auto Backend

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

3. API Documentation:
   Open http://localhost:8000/docs

## Modules

- **Project Management**: CRUD for projects.
- **Test Case Management**: Support for API, UI, and Performance cases.
- **Execution**: Task runner core.

## Configuration

Check `.env` for database and celery settings.
