#!/bin/bash

# Create the base directory for the project
mkdir -p my_project/alembic/versions
mkdir -p my_project/app

# Create Alembic migration configuration files
touch my_project/alembic/env.py
touch my_project/alembic/script.py.mako

# Create main application files
touch my_project/app/__init__.py
touch my_project/app/models.py
touch my_project/app/database.py
touch my_project/app/crud.py
touch my_project/app/config.py

# Create migration folder
touch my_project/migrations/.gitkeep

# Create a requirements.txt file
echo "SQLAlchemy==2.0.9" > my_project/requirements.txt
echo "alembic==1.9.4" >> my_project/requirements.txt
echo "psycopg2-binary==2.9.3" >> my_project/requirements.txt

# Create a simple Dockerfile (optional)
touch my_project/Dockerfile
cat <<EOL > my_project/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]
EOL

# Create a README.md file
touch my_project/README.md
cat <<EOL > my_project/README.md
# SQLAlchemy Project

This is a basic project template to use with SQLAlchemy, Alembic, and PostgreSQL.

## Setup

1. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. Initialize Alembic:
   \`\`\`bash
   alembic init alembic
   \`\`\`

3. Update the database connection string in \`alembic.ini\`.

4. Run migrations:
   \`\`\`bash
   alembic upgrade head
   \`\`\`
EOL

echo "Project directories and files have been created successfully!"