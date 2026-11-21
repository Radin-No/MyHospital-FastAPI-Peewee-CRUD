# Hospital Management Test System (FastAPI & Peewee)

A simple FastAPI app using the hospital ERD and SQLite.

- Full CRUD support.
- The database and initial sample records are created on launch.
- Install with `python -m pip install -r requirements.txt`.
- Run `python -m uvicorn main:app --reload` and visit http://localhost:8000/docs.
- The table names are listed at http://localhost:8000/. Use JSON bodies with the fields shown in `main.py`; foreign keys use their numeric IDs.
