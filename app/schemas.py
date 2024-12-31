from pydantic import BaseModel

class CompanyCreate(BaseModel):
    name: str
    address: str = None