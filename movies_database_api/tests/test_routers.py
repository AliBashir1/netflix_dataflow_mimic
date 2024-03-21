from movies_database_api.src.movies_api_main import app
from fastapi.testclient import TestClient
from movies_database_api.src.utilities.api_key import get_api_key
import pytest


def test_authentication():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code != 200
    assert response.json() == {'detail': 'Not authenticated'}

    response = client.get("/", headers={"x-access-token": "wrong_key"})
    assert response.status_code != 200
    assert response.json() == {'detail': 'Could not validate the access token.'}

    response = client.get("/", headers={"x-access-token": get_api_key()})
    assert response.status_code == 200
    assert response.json() == {"message": "welcome to movies app database."}


@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    client.headers = {"x-access-token": get_api_key()}
    return client


# user router tests
def test_users_by_id(client):
    response = client.get("/users/10001?does_account_exists=False")
    # 200 means user found and 404 means user not found
    assert response.status_code == 200 or response.status_code == 404

    if response.status_code == 200:
        expected_result = ['id', 'first_name', 'last_name', 'city', 'country', 'does_account_exists']
        result = list(response.json().keys())
        assert result == expected_result
    if response.status_code == 404:
        assert response.headers["x-message"] == "There is no user with id: 10001."

    # 10001 >= user id >= 499999

    response = client.get("/users/1")
    assert response.status_code == 422
    assert response.json() == {"detail": [
        {"type": "greater_than", "loc": ["path", "user_id"], "msg": "Input should be greater than 10000", "input": "1",
         "ctx": {"gt": 10000}, "url": "https://errors.pydantic.dev/2.4/v/greater_than"}]}

    response = client.get("/users/500000")
    assert response.status_code == 422
    assert response.json() == {"detail": [
        {"type": "less_than", "loc": ["path", "user_id"], "msg": "Input should be less than 500000", "input": "500000",
         "ctx": {"lt": 500000}, "url": "https://errors.pydantic.dev/2.4/v/less_than"}]}
#
#
def test_random_users(client):
    response = client.get("/users/random_users/")
#     assert response.status_code == 200
    # four fields in a json object
    assert len(response.json()) / 6 == 1

    response = client.get("/users/random_users/?number_of_user=5")
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_random_user_by_country(client):
    # usa and united states are not same
    response = client.get("/users/random_by_country/usa")
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}
    response = client.get("/users/random_by_country/united states")
    assert response.status_code == 200
#

# account router tests

