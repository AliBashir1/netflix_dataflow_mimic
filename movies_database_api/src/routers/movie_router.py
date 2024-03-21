from typing import List, Union
from fastapi import APIRouter, Depends, Query, Path
from typing_extensions import Annotated
from movies_database_api.src.crud.movie_crud import (
    get_movie_by_id,
    get_random_n_movie,
    initiate_add_movies,
    initiate_delete_movies,
    get_random_avail_movie
)
from movies_database_api.src.models.movie import (
    MovieIn,
    MovieOut
)
from movies_database_api.src.dependencies.validations import (
    validate_language
)
from movies_database_api.src.models.commons import QueryLimit
from fastapi import HTTPException, status
from sqlalchemy.exc import DBAPIError, OperationalError

TAG = ["Movies"]
movie_router = APIRouter()


@movie_router.get(
    "/movies/{movie_id}",
    tags=TAG,
    description="Find movie by id.",
    response_model=MovieOut
)
async def movie_by_id(movie_id: int):
    response = await get_movie_by_id(movie_id=movie_id)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no movie with id: {movie_id}"
        )

    return response


# random movie
@movie_router.get(
    "/movies/random_n_movie/",
    tags=TAG,
    response_model=Union[MovieOut, List[MovieOut]],
)
async def random_n_movie(
        number_of_movies: Annotated[int,Query(ge=1, le=10)] = 1,
        is_available: bool = True
):
    response = await get_random_n_movie(
        number_of_movies, is_available
    )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data available."
        )
    return response

@movie_router.get(
    "/movies/random_movie_by_language/",
    tags=TAG,
    response_model=MovieOut,
)
async def random_n_movie(
        language: Annotated[str, Depends(validate_language)] = 1
):
    response = await get_random_avail_movie(language)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data available."
        )
    return response


#
# # add movie to db -- just add date_added column
@movie_router.post(
    "/movies/set_n_movies_availability_by_language/{language}",
    response_model=dict,
    tags=TAG
)
async def add_movies(
        number_of_movies: Annotated[
            int,
            Query(ge=QueryLimit.min,le=QueryLimit.max)
        ],
        language: Annotated[str,Depends(validate_language)]
):
    response = await  initiate_add_movies(number_of_movies, language)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies available by language: {}.".format(language)
        )
    return response

# set false to is_available movies
@movie_router.delete(
    "/movies/delete_movies/{language}",
    response_model=dict,
    tags=TAG)
async def delete_movies(
    number_of_movies: Annotated[
        int, Query(ge=QueryLimit.min, le=QueryLimit.max)
    ],
    language:  Annotated[str, Depends(validate_language)]
):
    response = await  initiate_delete_movies(number_of_movies, language)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies available by language: {}.".format(language)
        )
    return response



