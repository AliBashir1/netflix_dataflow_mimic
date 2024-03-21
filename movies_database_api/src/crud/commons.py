from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, OperationalError
from fastapi.exceptions import HTTPException
from typing import Union, List, Dict, Callable, Any
from movies_database_api.src.utilities.movies_db_conn import get_movies_db_conn
from movies_database_api.src.models.user import User
from movies_database_api.src.models.account import AccountOut
from movies_database_api.src.models.movie import MovieOut


def select_query_executor(return_model_type: str):
    """
    A decorator to execute a query from the function
    """
    return_model_types = {
        "account": AccountOut,
        "user": User,
        "movie": MovieOut,
     }

    if return_model_type not in return_model_types:
        raise ValueError('Assign proper return type.')
    return_model = return_model_types[return_model_type]

    def query_executor(func):
        async def query_executor_wrapper(*args, **kwargs) -> Union[List[User], User, None]:
            query = await func(*args, **kwargs)
            try:
                engine = get_movies_db_conn()
                with engine.connect() as conn:
                    cursor_result = conn.execute(text(query), (args,))
                    if cursor_result.rowcount <= 0:
                        return None
                    elif cursor_result.rowcount == 1:
                        return return_model(**cursor_result.mappings().fetchone())
                    elif cursor_result.rowcount > 1:
                        return [return_model(**item) for item in cursor_result.mappings().fetchall()]
                    else:
                        return None
            except DBAPIError as e:
                raise DBAPIError(statement=e.statement, orig=e.orig, params=e.params)
            except OperationalError as e:
                raise OperationalError(statement=e.statement, orig=e.orig, params=e.params)

        return query_executor_wrapper

    return query_executor


def update_insert_query_executor(func):
    """
     A decorator to execute a query from the function
    """

    async def query_executor_wrapper(*args, **kwargs) -> Dict[str, Union[bool, Any]]:
        query = await func(*args, **kwargs)
        print("Insert or update query:\n",query)
        try:
            engine = get_movies_db_conn()
            with engine.connect() as conn:
                cursor_result = conn.execute(text(query))
                if cursor_result.rowcount > 0:
                    conn.commit()
                    return {
                        "status": 'success',
                    }
                else:
                    conn.rollback()


        except DBAPIError as e:
            raise DBAPIError(statement=e.statement, orig=e.orig, params=e.params)
        except OperationalError as e:
            raise OperationalError(statement=e.statement, orig=e.orig, params=e.params)

    return query_executor_wrapper

def proc_query_executor(func):
    async def query_executor_wrapper(*args, **kwargs) -> bool:
        query = await func(*args, **kwargs)
        print("Calling procedure:\n",query)
        try:
            engine = get_movies_db_conn()
            with engine.connect() as conn:
                cursor_result = conn.execute(text(query))
                # print("r\t", cursor_result.rowcount ,"\nf\t", cursor_result.fetchone()[0])
                if cursor_result.fetchone()[0] is True:
                    conn.commit()
                    return True
                else:
                    conn.rollback()
                    return False

        except DBAPIError as e:
            raise DBAPIError(statement=e.statement, orig=e.orig, params=e.params)
        except OperationalError as e:
            raise OperationalError(statement=e.statement, orig=e.orig, params=e.params)

    return query_executor_wrapper

