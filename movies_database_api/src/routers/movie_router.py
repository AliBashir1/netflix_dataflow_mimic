from fastapi import APIRouter, Depends, Query, Path
from typing_extensions import Annotated
from movies_database_api.src.crud.movie_crud import get_n_movies, get_random_movies
TAG = ["Movie"]
movie_router = APIRouter()


# random movie
@movie_router.get("/movies/random/", tags=TAG)
async def get_random_movie(number_of_movies: Annotated[int, Query( ge=1, le=10)] = 1):
    pass

# add movie to db -- just add date_added column
@movie_router.post("/movies/add_movies/{number_of_movies}")
async def add_movies(number_of_movies: Annotated[int, Path( ge=1, le=10)] = 1):

    pass


# search movies by genre
@movie_router.get("/movies/search_by_genre/{genre}")
async  def search_by_genre():
    pass
# by rating
# by title
