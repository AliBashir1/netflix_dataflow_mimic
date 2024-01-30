from configparser import ConfigParser
from typing import Union
from movies_database_api.src.utilities.root_dir import ROOT_DIR
import os


def get_config_parser() -> ConfigParser:
    """
    This function reads a conf.ini file, create config parses and returns it.
    :return: a config parser
    """
    # get an absolute path
    config_file: str = os.path.join(ROOT_DIR, "config", "movie_api_config.ini")
    config: Union[ ConfigParser, None ]= ConfigParser()
    config.read(config_file)

    if config is not None:
        return config
    else:
        raise ValueError("Config is none type.")


if __name__ == "__main__":
    get_config_parser()