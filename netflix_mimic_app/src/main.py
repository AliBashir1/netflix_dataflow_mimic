from netflix_mimic_app.src.user import User, UserHandler
from netflix_mimic_app.src.movie import MoviesHandler
from netflix_mimic_app.src.utilities.logs import get_logger
from netflix_mimic_app.src.commons import UserCount
from netflix_mimic_app.src.account import NewAccount, SetAccountStatus

from netflix_mimic_app.src.randomize_attributes import (
    RandCountry,
    RandNewAccountAttr,
    RandAccountExistence,
    RandLanguage
)

USER_LIMIT = 25000
def user_perc(
        *,
        active_user_count:int,
        paused_user_count: int,
        cancelled_user_count: int,
        user_counter: int

):
    active_perc = round((active_user_count/user_counter) * 100)
    paused_perc = round((paused_user_count/user_counter) * 100)
    cancelled_perc = round((cancelled_user_count/user_counter) * 100)
    print(active_perc, paused_perc, cancelled_perc)
    if user_counter <= 50:
        return 1 # continue
    else:
        if active_perc < 90:
            return 1 # continue watching movie
        elif paused_perc < cancelled_perc:
            return 2 # pause user
        else:
            return 3  # cancel user


def main():
    user_counter = 2500
    active_user_count = 200
    paused_user_count = 10
    cancelled_user_count = 20


    while True:
        user_counter += 1
        # fetch random country and account attributes
        country = RandCountry(user_counter).get_random_country()
        does_account_exists = RandAccountExistence(user_counter).get_random_account_existence()
        print(country, does_account_exists)

        if does_account_exists:
            # user counter increments until it hits new account limits
            # then it will decrement if account already exists
            if user_counter >= UserCount.new_user_account_limit:
                user_counter -= 1

            # determines if user should watch/rate movie, or pause account, or cancel account
            next_move = user_perc(
                active_user_count=active_user_count,
                paused_user_count=paused_user_count,
                cancelled_user_count=cancelled_user_count,
                user_counter=user_counter
            )
            print(next_move)
            if next_move == 1:
                try:
                    # get random user
                    user_info = UserHandler(does_account_exists, country).fetch_user()
                    user = User(user_info["id"])
                    print(user_info)
                    # fetch user's country language and fetch movie accordily
                    movie_language = RandLanguage.random_country_lang(user_info["country"])
                    movie = MoviesHandler().get_random_avail_movie(language=movie_language)

                    # note: setup movie watchin list, it should pop up after viewing time over



                    user.rate_movie()
                    user.watch_movie()
                except Exception as e:
                    # todo log it
                    print(repr(e))
                    continue



            # else
                # pause account
                # cancel account
            pass

        else:
            new_account_attr = RandNewAccountAttr().generate_new_account_attributes()
            # get user with country and account status
            user = UserHandler(does_account_exists, country).fetch_user()
            # Create Account
            new_account = new_account_attr
            del new_account_attr
            new_account["user_id"] = user["id"]
            new_account = NewAccount(**new_account)
            new_account.create_account()
            active_user_count += 1

        break






if __name__ == "__main__":
    main()
    # p_user = 20
    # c_user = 10
    # a_user = 200
    # user_c = 250
    # r = user_perc(
    #     active_user_count=a_user,
    #     user_counter=user_c,
    #     paused_user_count=p_user,
    #     cancelled_user_count=c_user
    # )
    #
    # print(r)
