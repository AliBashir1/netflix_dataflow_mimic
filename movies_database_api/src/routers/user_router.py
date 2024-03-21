from fastapi import APIRouter, Path, Query, HTTPException, Depends, status
from typing import List, Union
from typing_extensions import Annotated

from movies_database_api.src.crud.user_crud import (
    user_by_id,
    random_n_user,
    random_n_users_by_country
)
from movies_database_api.src.dependencies.validations import validate_country_name
from movies_database_api.src.models.user import User
from movies_database_api.src.models.commons import UserIDRange, QueryLimit
TAG = ["Users"]
user_router = APIRouter()


@user_router.get(
    "/users/{user_id}",
    response_model=User,
    tags=TAG,
    description="Find user by id, id range from 10001 to 301024."
)
async def get_user_by_id(
        user_id: Annotated[int, Path(ge=UserIDRange.min, le=UserIDRange.max)]
):
    response = await user_by_id(user_id=user_id)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user with id: {}".format(user_id)
        )
    return response


@user_router.get(
    "/users/random_n_users/",
    response_model=Union[User, List[User]],
    tags=TAG,
    description="Query users using limit and is_active query parameters."
                "Limit cannot go above 20"
)
async def get_n_random_user(
        does_account_exists: bool = False,
        number_of_user: int = Query(ge=QueryLimit.min, le=QueryLimit.max)
):
    response = await random_n_user(does_account_exists, number_of_user)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data available."
        )
    return response


@user_router.get(
    "/users/random_n_user_by_country/{country}",
    response_model=Union[User, List[User], None],
    tags=TAG
)
async def get_n_user_by_country(
        country: Annotated[str, Depends(validate_country_name)],
        does_account_exists: bool = False,
        number_of_user:  int  =  Query(ge=QueryLimit.min, le=QueryLimit.max)
):
    response = await random_n_users_by_country(
        country=country,
        does_account_exists=does_account_exists,
        number_of_user=number_of_user
    )
    user_status = "active" if does_account_exists else "inactive"

    if response is None:
        raise HTTPException(
            status_code=204,
            detail=f"No {user_status} User is found from {country}."
        )
    # note: how to use partial content
    # if isinstance(response, list):
    #     if len(response) != number_of_user:
    #         raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT)
    # if isinstance(response, UserOut) and number_of_user > 1:
    #     raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT)
    return response
