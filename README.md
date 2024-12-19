# SQLAlchemy Project

This is a basic project template to use with SQLAlchemy, Alembic, and PostgreSQL.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize Alembic:
   ```bash
   alembic init alembic
   ```

3. Update the database connection string in `alembic.ini`.

4. Run migrations:
   ```bash
   alembic upgrade head
   ```
