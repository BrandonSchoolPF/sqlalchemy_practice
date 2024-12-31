from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLAL_DATABASE_URL = 'postgresql://postgres:secret@localhost/test_db'

engine = create_engine(
    SQLAL_DATABASE_URL, connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()