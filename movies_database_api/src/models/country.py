from pydantic import BaseModel


class Country(BaseModel):
    iso_id: str
    country_name: str

    class Config:
        str_to_lower = True
