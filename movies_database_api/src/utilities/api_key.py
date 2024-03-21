def get_api_key():
    with open("/secret/key.txt") as key_file:
        key = str(key_file.read().strip())
    return key if key else None

