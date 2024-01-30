from fastapi import APIRouter, Path, Query, HTTPException, Depends, status
from typing import List, Union
from typing_extensions import Annotated

from movies_database_api.src.crud.user_crud import user_by_id, random_user, random_users_by_country
from movies_database_api.src.dependencies.validations import validate_country_name
from movies_database_api.src.models.user import User

TAG = ["users"]
user_router = APIRouter()


@user_router.get("/users/{user_id}",
                 response_model=User,
                 tags=TAG,
                 description="Find user by id, id range from 10001 to 499999."
                 )
async def get_user_by_id(
        user_id: Annotated[int, Path(gt=10000, lt=500000)],
        does_account_exists: Annotated[bool, Query()] = False):
    response = await user_by_id(user_id=user_id, does_account_exists=does_account_exists)

    if does_account_exists:
        msg = f"There is account holder user with id {user_id}"
    else:
        msg = f"There is no user with id: {user_id}"

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg
        )
    return response


@user_router.get("/users/random_users/",
                 response_model=User,
                 tags=TAG,
                 description="Query users using limit and is_active query parameters."
                             "Limit cannot go above 20")
async def get_random_user(does_account_exists: bool = False):
    response = await random_user( does_account_exists=does_account_exists)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data available."
        )
    return response


@user_router.get("/users/random_by_country/{country}",
                 response_model= User,
                 tags=TAG)
async def get_user_by_country(country: Annotated[str, Depends(validate_country_name)],
                              does_account_exists: bool = False):

    response = await random_users_by_country(country=country,
                                             does_account_exists=does_account_exists)
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
