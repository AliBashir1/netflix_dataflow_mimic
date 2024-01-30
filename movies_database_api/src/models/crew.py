from pydantic import BaseModel
from commons import GenderEnum


class BaseCrewModel(BaseModel):
    id: int
    name: str
    gender: GenderEnum

    class Config:
        str_to_lower = True
        validate_assignment = True


class Actor(BaseCrewModel):
    pass


class Director(BaseCrewModel):
    pass
