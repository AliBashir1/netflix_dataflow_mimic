from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from typing_extensions import Annotated
from typing import Union, List

from movies_database_api.src.crud.account_crud import (create_account,
                                                       pause_account,
                                                       get_random_account,
                                                       get_account_by_user_id,
                                                       get_random_account_by_country)
from movies_database_api.src.models.account import AccountOut, AccountCreateModel
from movies_database_api.src.models.commons import AccountStatus
from movies_database_api.src.dependencies.validations import validate_country_name
from sqlalchemy.exc import DBAPIError, OperationalError



TAG = ["Accounts"]
account_router = APIRouter()


@account_router.post(path="/accounts/create_account",
                     tags=TAG)
async def initiate_user_account(account: AccountCreateModel) -> None:
    try:
        response = await create_account(account)

        if not response:
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="account is not created.")
        else:
            raise HTTPException(status_code=status.HTTP_201_CREATED)

    except (DBAPIError, OperationalError) as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(e))


@account_router.post(path="/accounts/modify_account_status/{user_id}/{account_status}",
                     tags=TAG,
                     description="Fetch a user using a user id and account status.")
async def set_account_st(user_id: Annotated[int, Path(ge=10001, le=499999)],
                         account_status: AccountStatus) -> Union[dict, None]:
    try:
        updated = await pause_account(user_id, account_status)

        if not updated:
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                                detail="Changes are not updated in the account.")

        return {
            "user_id": user_id,
            "account_status": account_status
            }

    except (DBAPIError, OperationalError) as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(e))


@account_router.get("/accounts/random/",
                    response_model=Union[AccountOut, List[AccountOut]],
                    tags=TAG,
                    description="Fetch a random account or list of random account."
                                "The limit to number of account is 1 to 10.")
async def random_account(number_of_accounts: Annotated[int, Query(ge=1, le=10)] = 1,
                         account_status: AccountStatus = AccountStatus.active):
    try:
        account = await get_random_account(account_status=account_status, number_of_accounts=number_of_accounts)

        if account is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No account is found with {account_status}")
        return account

    except (DBAPIError, OperationalError) as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(e))


@account_router.get("/accounts/{user_id}/",
                    response_model=Union[AccountOut, List[AccountOut]],
                    tags=TAG,
                    description="Fetch an account by user_id. user_id is between 10001 to 499999.")
async def account_by_user_id(user_id: Annotated[int, Path(ge=10001, le=499999)],
                             account_status: AccountStatus = AccountStatus.active):
    try:
        account = await get_account_by_user_id(user_id=user_id, account_status=account_status)

        if account is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No account is found with user_id: {user_id} and account_status: {account_status}")
        return account

    except (DBAPIError, OperationalError) as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(e))


@account_router.get("/accounts/random_by_country/{country}",
                    response_model=Union[AccountOut, List[AccountOut]],
                    tags=TAG,
                    description="Fetch a random account or list of random account."
                                "The limit to number of account is 1 to 10.")
async def random_account_by_country(country: Annotated[str, Depends(validate_country_name)],
                                    number_of_accounts: Annotated[int, Query(ge=1, le=10)] = 1,
                                    account_status: AccountStatus = AccountStatus.active):
    try:
        account = await get_random_account_by_country(country=country, account_status=account_status,
                                                      number_of_accounts=number_of_accounts)
        if account is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No account is found with {account_status} status in {country}")
        return account

    except (DBAPIError, OperationalError) as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(e))
