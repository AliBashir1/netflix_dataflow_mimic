from cryptography.fernet import Fernet, InvalidToken
from configparser import ConfigParser
from typing import Union
from movies_database_api.src.utilities.config_parser import get_config_parser


def decrypt(encrypted_password: str = None) -> str:
    """
    The function shall decrypt the encrypted password and return it in string format.
    :param encrypted_password: A string of the encrypted password.
    :return: A string
    """
    config: ConfigParser = get_config_parser()
    key: Union[str, None] = config.get("KEY", "KEY")
    # convert key and encrypted password to the bytes object using utf-8 coding
    key: Union[bytes, None]  = bytes(key, "utf-8")
    encrypted_password: Union[bytes, None]  = bytes(encrypted_password, "utf-8")

    try:
        cipher_suite: Union[Fernet, None] = Fernet(key)
        decrypted_password: bytes = cipher_suite.decrypt(encrypted_password)
        plain_text_password: str = bytes(decrypted_password).decode("utf-8")
    except (InvalidToken, TypeError) as e:
        raise e

    if plain_text_password:
        return plain_text_password
    else:
        raise ValueError("plain_text_password is None type")


if __name__ == "__main__":
    a=decrypt('gAAAAABlFMtXpPhm74qaVpnveGID0ymjWN0tgX7sJsr6EFh4nGyVY29ilZnlz8Su5HQ2l2t-4_lw2W6VCFO3-gHHiUBk5s0gC5SW4qpFfSyg9RHfbD-7v8lY3IqjHFcG7NXqUuV-sQTh82hGyhkeL00wXH2EKTOrkr7sgWHEXbEJe3gS7687zAA=')
    print(a)