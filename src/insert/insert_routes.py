from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import CompanyCreate
from app.database import SessionLocal
from app.models import Company
from app.get_db import get_db


insert_router = APIRouter()


@insert_router.post("/companies", response_model=CompanyCreate)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.name == company.name).first()
    if db_company:
        raise HTTPException(status_code=400, detail="Company already exists")
    try:
        new_company = Company(name=company.name, address=company.address)
        
        db.add(new_company)
        db.commit()
        db.refresh(new_company)

        return new_company
    except Exception as exc:
        print('Could not add... Error: %s', exc)
