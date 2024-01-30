from movies_database_api.src.crud.commons import select_query_executor
from psycopg2 import sql


# todo: how to implement DRY in following codes.s

@select_query_executor(return_model_type='user')
async def user_by_id(*,
                     user_id: int,
                     does_account_exists: bool = False) -> str:
    if does_account_exists:
        join_type = 'inner'
    else:
        join_type = 'left'

    q = """
              SELECT 
                u.id,
                u.first_name,
                u.last_name,
                u.city,
                u.country,
                u.does_account_exists
             FROM users u
                 {} join accounts a on a.user_id = u.id
             WHERE u.id = {};
         """.format(join_type, user_id)
    return q


@select_query_executor(return_model_type='user')
async def random_users_by_country(*,
                                  country: str,
                                  does_account_exists: bool = False) -> str:
    if does_account_exists:
        join_type = 'inner'
    else:
        join_type = 'left'

    q = """
        SELECT 
            u.id,
            u.first_name,
            u.last_name,
            u.city,
            u.country,
            u.does_account_exists
        FROM users u
            {} join accounts a on a.user_id =u.id
        WHERE u.country = '{}' 
        ORDER BY random()
        LIMIT 1;
        
    """.format(join_type, country)
    return q


@select_query_executor(return_model_type='user')
async def random_user(*,does_account_exists: bool = False) -> str:
    if does_account_exists:
        join_type = 'inner'
    else:
        join_type = 'left'

    q = """
            SELECT 
                u.id ,
                u.first_name,
                u.last_name,
                u.city,
                u.country,
                u.does_account_exists
            FROM 
                users u
                {} join accounts a on a.user_id = u.id
            ORDER BY random() 
            limit 1
            """.format(join_type)

    return q

if __name__ == "__main__":
    import asyncio

    asyncio.run(user_by_id(user_id=10001))
