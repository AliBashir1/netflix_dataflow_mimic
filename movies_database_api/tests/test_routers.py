# from movies_database_api.src.movies_api_main import app
# from fastapi.testclient import TestClient
#
# client = TestClient(app)
#
#
# # testing main app
# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"test": "what"}
#
#
# # # user
# def test_users_by_id():
#     # check user
#     # 204
#     response = client.get("/users/10001?does_account_exists=False")
#     assert response.status_code == 200 or response.status_code == 404
#     if response.status_code == 200:
#         assert response.json() == {"id": 10001, "does_account_exists": "false", "city": "new york city",
#                                    "country": "usa"}
#     if response.status_code == 404:
#         assert response.headers["x-message"] == "There is no user with id: 10001."
#
#     # 10001 >= user id >= 499999
#
#     response = client.get("/users/1")
#     assert response.status_code == 422
#     assert response.json() == {"detail": [
#         {"type": "greater_than", "loc": ["path", "user_id"], "msg": "Input should be greater than 10000", "input": "1",
#          "ctx": {"gt": 10000}, "url": "https://errors.pydantic.dev/2.4/v/greater_than"}]}
#
#     response = client.get("/users/500000")
#     assert response.status_code == 422
#     assert response.json() == {"detail": [
#         {"type": "less_than", "loc": ["path", "user_id"], "msg": "Input should be less than 500000", "input": "500000",
#          "ctx": {"lt": 500000}, "url": "https://errors.pydantic.dev/2.4/v/less_than"}]}
#
#
# def test_random_users():
#     response = client.get("/users/random_users/")
#     assert response.status_code == 200
#     # four fields in a json object
#     assert len(response.json()) / 4 == 1
#
#     response = client.get("/users/random_users/?number_of_user=5")
#     assert response.status_code == 200
#     assert len(response.json()) == 5
#
#
# def test_random_user_by_country():
#     response = client.get("/users/random_by_country/usa")
#     assert response.status_code == 200
