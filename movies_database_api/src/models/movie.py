from pydantic import BaseModel, field_validator
from datetime import date, datetime as dt


class Movie(BaseModel):
    id: int
    title: str
    genres: str
    language: str
    popularity: float
    imdb_vote_count: float
    imdb_vote_average: float
    revenue: int
    budget: int
    release_date: date
    is_available: bool
    runtime: int
    date_added: date

    class Config:
        str_to_lower = True
        validate_assignment = True


class MovieIn(BaseModel):
    id: int


class MovieOut(BaseModel):
    id: int
    title: str
    genres: str
    language: str
    release_date: date
    is_available: bool
    date_added: date
    runtime: int
