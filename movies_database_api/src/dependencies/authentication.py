from fastapi import status, HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY = None
API_KEY_NAME = "x-access-token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def verify_access_token(api_access_token: str = Security(api_key_header)):

    with open("/secret/key.txt") as key_file:
        global API_KEY
        API_KEY = str(key_file.read().strip())

    if api_access_token != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate the access token.")
    return api_access_token
