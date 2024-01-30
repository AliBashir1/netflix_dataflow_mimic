from pydantic import BaseModel


class Company(BaseModel):
    id: int
    company_name: str
    parent_company: str

    class Config:
        str_to_lower = True
