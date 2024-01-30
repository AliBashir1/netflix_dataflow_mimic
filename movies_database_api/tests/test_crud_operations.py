from movies_database_api.src.crud.user_crud import user_by_id, random_user, random_users_by_country
from movies_database_api.src.models.user import UserOut
import pytest



# note: write test for exceptions as well

#
@pytest.mark.asyncio
async def test_user_by_id():
    user = await user_by_id(user_id=100001)
    assert isinstance(user, UserOut)

    # no user exists with user_id 1
    user = await user_by_id(user_id=1)
    assert user is None

    # no user exists with user_id 500000
    user = await user_by_id(user_id=500000)
    assert user is None


@pytest.mark.asyncio
async def test_random_users_by_country():
    # extract one user from uae
    user = await random_users_by_country(country='uae')
    assert isinstance(user, UserOut)

    # extract multiple users from uae
    list_of_user = await random_users_by_country(country='usa', number_of_user=3)
    assert isinstance(list_of_user, list)

    user = list_of_user[0]
    assert isinstance(user, UserOut)

    user = await random_users_by_country(country="doesnt exists")
    assert user is None


#


@pytest.mark.asyncio
async def test_random_user():
    # with pytest.raises(DBAPIError) as e:
    #     # create custom exception to check if exception is being raised
    #
    #     await user_by_id(user_id=10001)
    # if e.value:
    #     assert e.value == "error in database"
    #     pytest.mark.skip("skip everything")

    user = await random_user()
    assert isinstance(user, UserOut)

    list_of_user = await random_user(number_of_user=3)
    assert isinstance(list_of_user, list)

    user = list_of_user[0]
    assert isinstance(user, UserOut)

    user = await random_user(number_of_user=0)
    assert user is None
