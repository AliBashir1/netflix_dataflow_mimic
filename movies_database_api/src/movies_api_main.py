from fastapi import FastAPI, Depends
from movies_database_api.src.routers.user_router import user_router
from movies_database_api.src.routers.account_router import account_router
from movies_database_api.src.routers.movie_router import movie_router
from movies_database_api.src.dependencies.authentication import verify_access_token


app = FastAPI(dependencies=[Depends(verify_access_token)])

app.include_router(account_router)
app.include_router(user_router)
app.include_router(movie_router)


@app.get("/")
async def root_dir():
    return {"message": "welcome to movies app database."}


if __name__ == "__main__":
    pass
    # from movies_database_api.src.utilities.movies_db_conn import get_movies_db_conn
    # from movies_database_api.src.models.user import UserOut
    # from sqlalchemy.exc import DBAPIError, OperationalError
    # from typing import Union, List
    # from sqlalchemy import text
    #
    #
    # def query_executor(func):
    #     async def query_executor_wrapper(*args, **kwargs) -> Union[List[UserOut], UserOut, None]:
    #         query = await func(*args, **kwargs)
    #         try:
    #             engine = get_movies_db_conn()
    #             with engine.connect() as conn:
    #                 cursor_result = conn.execute(text(query))
    #
    #                 if cursor_result.rowcount <= 0:
    #                     return None
    #                 elif cursor_result.rowcount == 1:
    #                     return UserOut(**cursor_result.mappings().fetchone())
    #                 elif cursor_result.rowcount > 1:
    #                     return [UserOut(**item) for item in cursor_result.mappings().fetchall()]
    #                 else:
    #                     return None
    #         except DBAPIError as e:
    #             print(e.statement)
    #             raise DBAPIError(statement="error in database", orig=e.orig, params=e.params)
    #         except OperationalError as e:
    #             print(e.statement)
    #             raise OperationalError(statement="error in operations", orig=e.orig, params=e.params)
    #
    #     return query_executor_wrapper
    #
    #
    # import asyncio
    #
    #
    # @query_executor
    # async def get_user_by_id(user_id, does_account_exists):
    #     return f"""SELECT
    #                     id,
    #                     city,
    #                     country,
    #                     does_account_exists
    #                 FROM users
    #                 WHERE ID = {user_id} and does_account_exists = {does_account_exists} """
    #
    # async def main():
    #     a = await get_user_by_id(user_id=100001, does_account_exists=True)
    #     print(a)
    # asyncio.run(main())
