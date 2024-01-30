from __future__ import annotations

from netflix_mimic_app.src.movie import Movie
import random
import requests
import json
class BaseUser:
    def __init__(self, user_id: int):
        self._key: None | str = self._get_api_key()
        self._baseurl : str = 'http://movies_api:8000'
        self.user_id: int | None = user_id

    def _get_api_key(self):
        with open("/secret/key.txt") as key_file:
            key = str(key_file.read().strip())
        return key if key else None
class NewUser(BaseUser):
    def __init__(self, user_id: int):
        super().__init__(user_id)
        self.does_account_exists = True
        self.billing_type = random.choices(["monthly", "yearly"], weights=[0.7, 0.3])[0]
        self.payment_method = random.choices(["credit", "debit", "checking"], weights=[0.3, 0.3, 0.4])[0]
        self.device_type = random.choices(["mobile", "tv", "computer"], weights=[0.1, 0.4, 0.5])[0]
        self.account_status = 'active'
    def create_account(self):
        url = self._baseurl + "/accounts/create_account"
        data = {**self.__dict__}
        del data["_key"], data["_baseurl"], data["does_account_exists"]

        res = requests.post(url,headers={"x-access-token": self._key}, data=json.dumps(data))

        if res.status_code == 201:
            # return user data
            new_user_data = requests.get(self._baseurl + "/users/{}".format(self.user_id),
                                         headers={"x-access-token": self._key}).json()
            new_user_data["user_id"] = new_user_data["id"]
            del new_user_data["id"]
            return  new_user_data

        else:
            raise ValueError("Account not created")
class SubscribedUser(BaseUser):
    def __init__(self, user_id: int, first_name: str, last_name: str, city: str, country: str, does_account_exists: bool = True):
        super().__init__(user_id=user_id)
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.country = country
        self.does_account_exists = does_account_exists

    def modify_account_status(self, new_status: str = "paused"):
        url = self._baseurl + "/accounts/modify_account_status/{}/{}".format(self.user_id, new_status)
        res = requests.post(url,headers={"x-access-token": self._key})
        if res.status_code == 200 :
            return self.__dict__
        else:
            raise ValueError("Account of user_id: {} is not {}".format(self.user_id,new_status))
    def get_account_status(self):
        url = self._baseurl + "/accounts/get_account_status/{}".format(self.user_id)
        res = requests.get(url,headers={"x-access-token": self._key})
        if res.status_code == 200 :
            return res.json()
        else:
            raise ValueError("Account not paused")

    def watch_movie(self, movie: Movie):
        # put user to sleep to pretend it use watching movie
        # put it to sleep for 1/10 of movie length

        pass

    def rate_movie(self, movie_id: int):
        # randomly rate it
        # confirm if user has watched the movie
        pass
