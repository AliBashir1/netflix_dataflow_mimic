from datetime import datetime as dt
from movies_database_api.src.crud.commons import select_query_executor, update_insert_query_executor


@select_query_executor(return_model_type='movie')
async def get_movie_by_id(movie_id: int) -> str:
    q = """
        SELECT 
            m.id,
            m.title,
            m.genres,
            m.language,
            m.release_date,
            m.is_available,
            m.date_added
        FROM movies m
        WHERE m.id = {};
    """.format(movie_id)
    return q


@select_query_executor(return_model_type='movie')
async def get_random_n_movie(
        number_of_movies: int = 1,
        is_available: bool = False
) -> str:
    q = """
        SELECT 
            m.id,
            m.title,
            m.genres,
            m.language,
            m.release_date,
            m.is_available,
            m.date_added
        FROM movies m
        WHERE m.is_available = {}
        ORDER BY RANDOM()
        LIMIT {};
    """.format(is_available, number_of_movies)
    return q


@update_insert_query_executor
async def initiate_add_movies(
        number_of_movies: int,
        language: str
) -> str:
    date = dt.today().strftime('%Y-%m-%d')
    q = """
            WITH  random_movie AS  ( 
                    SELECT  
                        id 
                    FROM  
                        movies 
                    WHERE language = '{}' and is_available = false
                    ORDER  BY random() 
                    limit {}
                    )
            UPDATE movies 
            SET date_added = '{}', is_available = true
            WHERE id IN (SELECT id FROM random_movie)
            """.format(language, number_of_movies, date)
    return q

@update_insert_query_executor
async def initiate_delete_movies( number_of_movies: int,
        language: str
) -> str:
    date = '1900-01-01'
    q = """
            WITH  random_movie AS  ( 
                    SELECT  
                        id 
                    FROM  
                        movies 
                    WHERE language = '{}' and is_available = true
                    ORDER  BY random() 
                    limit {}
                    )
            UPDATE movies 
            SET date_added = '{}', is_available = false
            WHERE id IN (SELECT id FROM random_movie)
            """.format(language, number_of_movies, date)
    return q
@select_query_executor(return_model_type='movie')
async def get_random_avail_movie(
        language: str = 'English'
) -> str:
    q = """
        SELECT 
            m.id,
            m.title,
            m.genres,
            m.language,
            m.release_date,
            m.is_available,
            m.date_added,
            m.runtime
        FROM movies m
        WHERE m.language = '{}' and m.is_available = True
        ORDER BY RANDOM()
        LIMIT 1;
    """.format(language)
    return q
