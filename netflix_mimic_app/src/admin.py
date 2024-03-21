from netflix_mimic_app.src.user import NewUser, ActiveUser
from netflix_mimic_app.src.randomize_attributes import RandomAccountCountry
import random


class Admin:
    def __init__(self):
        (
            self.does_account_exist,
            self.country,
            self.account_status
         ) = RandomAccountCountry.get_random_country_n_account()
        # should I use New Account or NewUser ?
        # new account make more sense, It will just create the new users and return a user id
        # if user doesnt exists then cater it according to self.account_status
        # may be create seperate classes for paused_account and cancelled account.
        self.user = NewUser if self.does_account_exist else ActiveUser


if __name__ == "__main__":
    a = Admin()
    print(a.country, a.does_account_exist)