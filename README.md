# SQLAlchemy Project

This is a basic project template to use with SQLAlchemy, Alembic, and PostgreSQL. 
This will be a reference that I will use to see the methods used to create and setup a postgres server on docker, sqlalchemy and alembic

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

2. Initialize Alembic:
   ```bash
   alembic init alembic
   ```

3. Update the database connection string in `alembic.ini`.

4. Run migrations:
   ```bash
   alembic upgrade head
   ```
