from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import CompanyCreate
from app.database import SessionLocal
from app.models import Company
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/companies/", response_model=CompanyCreate)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.name == company.name).first()
    if db_company:
        raise HTTPException(status_code=400, detail="Company already exists")

    new_company = Company(name=company.name, address=company.address)
    
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


@app.post("/addtest/", response_model=TestCreate)
def add_test()