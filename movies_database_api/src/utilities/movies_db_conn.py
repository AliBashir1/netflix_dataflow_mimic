from configparser import ConfigParser
from sqlalchemy import create_engine, text

from movies_database_api.src.utilities.encryption import decrypt
from movies_database_api.src.utilities.config_parser import get_config_parser

from movies_database_api.src.models.commons import AccountStatus


def get_movies_db_conn():
    config: ConfigParser = get_config_parser()
    # Encrypted connection string
    con_str: str = config.get("MOVIES_DB_DEV", "movie_db_conn_str")

    # decrypt connection string using key
    d_con_str: str = decrypt(con_str)

    # row_factory=dict_row returns results as dictionary
    engine = create_engine(d_con_str)
    return engine


if __name__ == "__main__":
    conn = get_movies_db_conn().raw_connection()

    q = f"""
         call update_account_status(user_id_in := {10002},new_account_status := '{AccountStatus.pause}'::account_status );
    """
    curr = conn.cursor()
    conn.commit()

