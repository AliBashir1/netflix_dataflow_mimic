from pydantic import BaseModel, BaseConfig, Field, Alias


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    city: str
    country: str
    does_account_exists: bool
    class Config:
        str_to_lower = True
        validate_assignment = True

