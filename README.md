# SQLAlchemy Project

This is a basic project template to use with SQLAlchemy, Alembic, and PostgreSQL. 
This will be a reference that I will use to see the methods used to create and setup a postgres server on docker, sqlalchemy and alembic

Sqlalchemy is a way to manipulate a database through python, Alembic is like the git of database for sqlalchemy, alembic has the ability to revert and migrate (git push, pull, revert). The main functions of alembic are: 

```bash
alembic init {folder_name_here} #This initializes the alembic package
alembic current #Shows the current version the DB is on
alembic upgrade head #Ugrades DB to the most current version (git pull)
alembic downgrade -1 #Downgrades the DB one version down
alembic revision --autogenerate -m 'YOUR_MESSAGE_HERE' #Alembic will view your changes and update the db automatically
```


This will show the user how to run postgres __on docker__ not locally

## Process Flow
Note that this is meant for Postgres, havent used anything else

1. Setting up the Docker Container
* Install Docker then install the postgres package with this command: 
   ```bash
   docker pull postgres
   ```
   This will install the necessary packages needed for docker to run a postgres server

2. Create a container:
   ```bash
   docker image #Check if Postgres is running

   docker run --name 'CONTAINER_NAME' -p 5432:5432 -e POSTGRES_PASSWORD='your_password' -d postgres
   ```
   -p represents the port it will be hosted on, -e represents the encryption, and -d means that it will run in the background to free up terminal

3. Create a database on container:
   ```bash
   docker exec -ti 'CONTAINER_NAME' createdb -U postgres 'DATABASE_NAME_HERE'
   ```

4. Stopping the Docker Container:
   ```bash
   #Check the list of running containers
   docker ps
   ```
   The docker ps will give a container id and name which will be used to tell docker which container to stop
   ```bash
   docker stop 'container_id_or_name'
   ```

5. Starting the container:
   ```bash
   docker start 'container_id_or_name'
   ```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   __If you cannot install psycopg2, sudo or brew postgres__

2. Initialize Alembic:
   ```bash
   alembic init alembic
   ```

3. Update the database connection string in `alembic.ini`.
   ```python
   sqlalchemy.url = postgresql://postgres:secret@localhost/{db_name_here}
   ```

4. Create a Base class and create a model in whichever file using sqlalchemy like so: 
   ```python
   from sqlalchemy import Column, DateTime, String, Integer, func
   from sqlalchemy.ext.declarative import declarative_base

   Base = declarative_base()
   metadata = Base.metadata

   class Company(Base):
      __tablename__='company'

      id = Column(Integer, primary_key=True)
      name = Column(String(60), unique=True)
      address = Column(String(100), nullable=True)
      created_at = Column(DateTime, default=func.now())

      def __repr__(self) -> str:
         return f"id: {self.id}, name: {self.name}"
   ```
   The following code produces a table which contains the columns id, name, address, and created_at. To use alembic to upgrade the postgres db, go into the env.py file within the folder that was created from ```alembic init {your folder name}```

   ```python
   from logging.config import fileConfig

   from sqlalchemy import engine_from_config
   from sqlalchemy import pool
   from app.models import Base #Reference your declarative base model here
   from alembic import context

   # this is the Alembic Config object, which provides
   # access to the values within the .ini file in use.
   config = context.config

   # Interpret the config file for Python logging.
   # This line sets up loggers basically.
   if config.config_file_name is not None:
      fileConfig(config.config_file_name)

   # add your model's MetaData object here
   # for 'autogenerate' support
   # from myapp import mymodel
   # target_metadata = mymodel.Base.metadata
   target_metadata = Base.metadata #Add the metadata method from the base class
   ```
6. To autogenerate changes to the DB simply use the autogenerate function: 
   ```bash
   alembic revision --autogenerate -m 'your_message_here'
   ```

   To view your changes simply run the docker exec command to open up psql on terminal: 

   ```bash
   docker exec -ti {container_name} psql -U postgres -d {DB_name}
   ```

# Connecting SQLAlchemy to Postgres using Fast API
SQLAlchemy is just a tool to get SQL statements into Python. Actions like SELECT, JOIN, etc..
have been built into SQLAlchemy. FastAPI is an API builder which allows the user to create HTTP requests (POST, GET).
FastAPI combined with SQLAlchemy can allow the user to create queries or inserts through API requests through FastAPI

__*Note that you will not need to manually push new tables into postgres with SQLAlchemy if you are using alembic to auto migrate the tables*__

## __Setting up DB Connection with SQLAlchemy__

With SQLAlchemy, the objects required to speak with any database are engine, SesionLocal, and Declarative base.

* __engine()__

   The engine in SQLAlchemy is the starting point for interacting with your database. It provides the interface to communicate with your database and allows you to execute SQL queries.

   To create an engine, use the create_engine function, which takes a database URL (connection string) as an argument. The connection string should contain details like the database type, username, password, host, and database name.

   Example of creating an engine:

   ```python
   from sqlalchemy import create_engine

   # Example connection string for PostgreSQL
   DATABASE_URL = "postgresql://username:password@localhost/dbname"

   # Create the engine
   engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` will log all SQL queries for debugging
   ```

* __SessionLocal__

   SQLAlchemy uses sessions to manage transactions with the database. A session provides a "workspace" for the application where queries, inserts, updates, and deletes are stored before being committed to the database.

   You can create a SessionLocal class to manage database sessions. It is common to use a sessionmaker to create a session class bound to the engine.

   Example of setting up SessionLocal:

   ```python
   from sqlalchemy.orm import sessionmaker

   # Create a session factory bound to the engine
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   ```

   * ```autocommit=False```: Disables automatic commit after each operation. This gives you more control over when to commit or rollback transactions.
   * ```autoflush=False```: Disables automatic flushing of the session after each query. This can be helpful in complex operations where you want to flush explicitly.
   * ```bind=engine```: Binds the session to the engine you created earlier, which is required for the session to communicate with the database.

* __declarative_base__

   SQLAlchemy uses declarative base to define the structure of your tables. It allows you to define your database models as Python classes. These classes should inherit from a base class, typically called ```Base```.

   First, create a Declarative Base class using ```declarative_base()``` from SQLAlchemy:

   ```python
   from sqlalchemy.ext.declarative import declarative_base

   # Create the declarative base
   Base = declarative_base()
   ```

Here is a template of how the db connection with SQLAlchemy should look like: 
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Set up engine (PostgreSQL in this example)
DATABASE_URL = "postgresql://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL, echo=True)

# 2. Create SessionLocal class to manage sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create a declarative base
Base = declarative_base()
```

## __Creating a FastAPI App__

This portion will go over creating the FastAPI app which is the entrypoint for communications between the DB and SQLAlchemy.

Here’s a summary of the most commonly used HTTP methods in web development:

| HTTP Method | Purpose                                    | Description |
|-------------|--------------------------------------------|-------------|
| `GET`       | Retrieve data                              | Requests data from the server (e.g., a list of users). |
| `POST`      | Create a new resource                      | Sends data to the server to create a new resource. |
| `PUT`       | Update an existing resource                | Replaces an existing resource with new data. |
| `PATCH`     | Partially update a resource                | Updates a resource with partial data (only modified fields). |
| `DELETE`    | Delete a resource                          | Removes a resource from the server. |

Each HTTP method serves a distinct purpose and is crucial for performing CRUD (Create, Read, Update, Delete) operations in web applications.

