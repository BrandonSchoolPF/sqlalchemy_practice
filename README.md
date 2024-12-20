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