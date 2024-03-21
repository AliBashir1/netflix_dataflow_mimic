from netflix_mimic_app.src.commons import send_request
class User:
    def __init__(self, user_id):
        self.user_id = user_id
        pass
    def watch_movie(self):
        print("watching movie")
    def rate_movie(self):
        print("rating movie")

# add fetch users information
# delete account aka set the does_account_exists to false etc

class UserHandler:
    def __init__(self,does_account_exists, country):
        self.does_account_exists = does_account_exists
        self.country = country

    @send_request(request_type="get")
    def fetch_user(self):
        rel_url = "/users/random_n_user_by_country/{}?does_account_exists={}&number_of_user={}".format(
            self.country,
            self.does_account_exists,
            1
        )
        return rel_url
