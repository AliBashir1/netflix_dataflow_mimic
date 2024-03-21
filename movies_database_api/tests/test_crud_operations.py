from movies_database_api.src.crud.user_crud import user_by_id, random_user, random_users_by_country
from movies_database_api.src.models.user import User
import pytest
from psycopg2 import connect, extensions,sql




# note: write test for exceptions as well
# setup and teardown for database and then run account dml operations
def setup_movies_db():
    with open("/netflix_mimic_app/movies_database_api/tests/resources/setup_test_movies_database.sql", "r") as f:
        setup_sql = f.read()
    conn = connect(
        dbname="postgres",
        user="alimalik",
        password="alimalik123!",
        host="movies_database",
        port="5432"
    )
    auto_commit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(auto_commit)

    cur = conn.cursor()

    cur.execute(sql.SQL("""CREATE ROLE "movies_app_test" WITH PASSWORD 'moviesapppassword' LOGIN;"""))
    cur.execute(sql.SQL("""CREATE DATABASE  test_movies_database;"""))
    cur.execute(sql.SQL(setup_sql))
    conn.commit()
    conn.close()


    # auto_commit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    # conn = get_movies_db_conn(type="admin").raw_connection()
    # conn.set_isolation_level(auto_commit)
    # cur = conn.cursor()
    # cur.execute(text("""CREATE ROLE "movies_app_test" WITH PASSWORD 'moviesapppassword' LOGIN;"""))
    # cur.execute(text("""CREATE DATABASE  test_movies_database;"""))
    # conn.execute(text(script))
    # conn.commit()

    conn.close()


#
# @pytest.mark.asyncio
# async def test_user_by_id():
#     user = await user_by_id(user_id=100001)
#     assert isinstance(user, User)
#
#     # no user exists with user_id 1
#     user = await user_by_id(user_id=1)
#     assert user is None
#
#     # no user exists with user_id 500000
#     user = await user_by_id(user_id=500000)
#     assert user is None
#

# @pytest.mark.asyncio
# async def test_random_users_by_country():
#     # extract one user from uae
#     user = await random_users_by_country(country='uae')
#     assert isinstance(user, User)
#
#     # extract multiple users from uae
#     list_of_user = await random_users_by_country(country='usa', number_of_user=3)
#     assert isinstance(list_of_user, list)
#
#     user = list_of_user[0]
#     assert isinstance(user, User)
#
#     user = await random_users_by_country(country="doesnt exists")
#     assert user is None
#
#
# #
#
#
# @pytest.mark.asyncio
# async def test_random_user():
#     # with pytest.raises(DBAPIError) as e:
#     #     # create custom exception to check if exception is being raised
#     #
#     #     await user_by_id(user_id=10001)
#     # if e.value:
#     #     assert e.value == "error in database"
#     #     pytest.mark.skip("skip everything")
#
#     user = await random_user()
#     assert isinstance(user, User)
#
#     list_of_user = await random_user(number_of_user=3)
#     assert isinstance(list_of_user, list)
#
#     user = list_of_user[0]
#     assert isinstance(user, User)
#
#     user = await random_user(number_of_user=0)
#     assert user is None

if __name__ == "__main__":
    setup_movies_db();
