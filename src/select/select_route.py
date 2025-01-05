from fastapi import APIRouter, Depends
from app.get_db import get_db
from sqlalchemy.orm import Session
from app.models import Company

get_data = APIRouter()

@get_data.get("/company_name/{company_id}")
def get_company_name(company_id, db: Session = Depends(get_db)):
    company_name = db.query(Company).filter(Company.id == company_id).first()
    print(company_name)
    if company_name:
        return {'Company ID': id, 'Company Name': company_name.name, 'Company Address':company_name.address, 'Date Created':company_name.created_at}
    else:
        return {f'Company {id} does not exist'}