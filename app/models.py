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


class test(Base):
    __tablename__='test'

    id = Column(Integer, primary_key=True)
    address = Column(String(60), unique=True)
    children = Column(String(100), nullable=True)
    gender = Column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}"