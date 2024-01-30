"""

Admin shall add new movies.

Admin shall store user’s location information.

City, state, and country.

Admin shall store user’s daily usage of the app.

The amount of time spent watching movies is considered as time spent.

Admin shall randomly pick a user and create an account for them.

Admin shall randomly pick a user and pause their account for them.

Admin shall randomly pick a user and resume their account for them.

Admin shall randomly pick a user and delete an account for them.

Admin shall store user’s device information.

Admin shall log following

Http requests

Admin’s activity (adding new users, deleting etc)
"""
from __future__ import annotations
from datetime import datetime
import logging
import random
import requests

# projects
from netflix_mimic_app.src.user import SubscribedUser , NewUser



class BaseAdmin:
    def __init__(self):
        self._key: str = self._get_api_key()
        self._baseurl: str = 'http://movies_api:8000'
        self.hot_country_list: list = ['United States', 'India', 'United Kingdom', 'Canada',
                                 'Australia', 'Germany', 'France', 'Japan', 'Italy',
                                   'Spain', 'Mexico', 'South Korea', 'Brazil']
        self.country_list: list = ['Argentina', 'Austria', 'Bangladesh', 'Bolivia', 'Chile',
                                   'Ecuador', 'Egypt', 'Greece', 'Hungary', 'Indonesia', 'Ireland', 'Israel', 'Kuwait',
                                   'Lebanon', 'Malaysia', 'Morocco', 'Netherlands', 'New zealand', 'Nigeria', 'Oman',
                                   'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Poland', 'Portugal', 'Puerto rico',
                                   'Russia', 'Saudi arabia', 'South africa', 'South korea', 'Sweden', 'Switzerland',
                                   'Turkey', 'United Arab Emirates', 'Uruguay', 'Venezuela', 'Zimbabwe']

        # self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(logging.INFO)
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # log_file = f"UserAdmin_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        # file_handler = logging.FileHandler(log_file)
        # file_handler.setLevel(logging.INFO)
        # file_handler.setFormatter(formatter)
        # self.logger.addHandler(file_handler)
    def _get_api_key(self):
        with open("/secret/key.txt") as key_file:
            key = str(key_file.read().strip())
        return key if key else None

class UserAdmin(BaseAdmin):
    counter: int = 0
    def __init__(self):
        super().__init__()
        UserAdmin.counter = UserAdmin.counter + 1
        subscribed_choice_weight = [0.1, 0.9] if UserAdmin.counter % 200 == 0 else [0.5, 0.5]
        self.is_subscribed: str = random.choices([True, False], weights=subscribed_choice_weight)[0]
        # first and every 10, 11th, and 12th user shall be from regular country
        self._selected_country_list: list =  ( self.country_list if UserAdmin.counter % 10 == 0
                                                           or UserAdmin.counter % 11 == 0
                                                           or UserAdmin.counter % 12 == 0
                                      else self.hot_country_list
                                      )
        self.country: str = random.choice(self._selected_country_list)
        self.user: NewUser | SubscribedUser | None = None

    def get_user_by_country(self):
        url = ( self._baseurl + "/users/random_by_country/{}?does_account_exists={}"
               .format(self.country, str(self.is_subscribed).lower())
               )
        res = requests.get(url,headers={"x-access-token": self._key})
        print(res.status_code)
        if res.status_code != 200 :
            raise ValueError("No user found")


        if not self.is_subscribed:
            self.user = NewUser(res.json()["id"])
        else:
            data = res.json()
            data["user_id"] = data["id"]
            del data["id"]
            self.user = SubscribedUser(**data)

    def new_user_activity(self):
        if isinstance(self.user, NewUser):
            self.user = SubscribedUser(**self.user.create_account())
            # log it
            print("New user created at {} from {}".format(datetime.now(),self.country))
        else:
            raise ValueError("User is not new user")
    def subscribed_user_activity(self):
        pass



    # def random_user(self, active_user: str = 'no'):
    #     """
    #     :param active_user: 'yes' or 'no'
    #     :return:
    #     """
    #     number_of_users: int = 1
    #     url = ( self._baseurl + "/users/random_users/?number_of_user={}&does_account_exists={}"
    #            .format(number_of_users, active_user)
    #            )
    #     res = requests.get(url,headers={"x-access-token": self._key})
    #     if res.status_code != 200 :
    #         raise ValueError("No user found")
    #
    #     user_data = res.json()
    #     if user_data["does_account_exists"] == False:
    #         self.user = NewUser(user_data["id"])
    #         self.user = self.user.create_account()
    #
    #     self.user = SubscribedUser(**user_data)


    def create_user_account(self):
        # randomly select between credit, debit or checking
        pass
        if ~ self.user.does_account_exists:
            pass
    def resume_user_account(self):
        pass
    def cancel_user_account(self):
        pass

    def stimulate_watcing_activity(self, user_id: int, movie_id: int):
        pass

class MovieAdmin:
    def __init__(self):
        pass
if __name__ == "__main__":
    admin = UserAdmin()
    admin.random_user('false')
