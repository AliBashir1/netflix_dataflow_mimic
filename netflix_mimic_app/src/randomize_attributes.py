import random
from netflix_mimic_app.src.commons import BillingType, AccountStatus, PaymentType,DeviceType, UserCount
from time import sleep

class RandCountry:
    def __init__(self, user_counter: int):
        """
        Initialize the RandCountry object.

        Args:
            user_counter (int): Number of users. Cannot be None.

        Raises:
            ValueError: If user_counter is None.
        """
        if user_counter is None:
            raise ValueError("user_counter cannot be none.")
        self.user_counter = user_counter

    def get_random_country(self):
        """
        Get a random country based on the user_counter.

        Returns:
            str: A randomly selected country.
        """
        # Hot country list is to simulate real-world scenario where 80% of the users are from hot countries.
        # United States users are the largest in this pool.
        country_with_higher_subs = {
            'United States': 0.7, 'India': 0.2, 'United Kingdom': 0.3, 'Canada': 0.3,
            'Australia': 0.2, 'Germany': 0.2, 'France': 0.1, 'Japan': 0.2, 'Italy': 0.1,
            'Spain': 0.1, 'Mexico': 0.3, 'South Korea': 0.2, 'Brazil': 0.2
        }

        country_with_lower_subs = {
            'Argentina': 0.2, 'Austria': 0.2, 'Bangladesh': 0.1, 'Bolivia': 0.2,
            'Chile': 0.3, 'Ecuador': 0.2, 'Egypt': 0.1, 'Greece': 0.2, 'Hungary': 0.3,
            'Indonesia': 0.2, 'Ireland': 0.3, 'Israel': 0.1, 'Kuwait': 0.2, 'Lebanon': 0.3,
            'Malaysia': 0.1, 'Morocco': 0.3, 'Netherlands': 0.3, 'New Zealand': 0.1,
            'Nigeria': 0.1, 'Oman': 0.3, 'Pakistan': 0.3, 'Panama': 0.2, 'Paraguay': 0.2,
            'Peru': 0.3, 'Poland': 0.3, 'Portugal': 0.3, 'Puerto Rico': 0.2, 'Russia': 0.3,
            'Saudi Arabia': 0.3, 'South Africa': 0.3, 'South Korea': 0.3, 'Sweden': 0.1,
            'Switzerland': 0.3, 'Turkey': 0.2, 'United Arab Emirates': 0.1, 'Uruguay': 0.3,
            'Venezuela': 0.2, 'Zimbabwe': 0.3
        }

        # About 80 percent accounts shall be from country_with_higher_subs
        selected_countries_list = (
            country_with_lower_subs if self.user_counter % 10 == 0
                                       or self.user_counter % 11 == 0
                                   else country_with_higher_subs
                                   )

        country = random.choices(
            list(selected_countries_list.keys()),
            weights=list(selected_countries_list.values())
        )

        return country[0]  # Return the selected country


class RandAccountExistence:
    def __init__(self, user_counter: int = None):
        """
        Initialize the RandAccountExistence object.

        Args:
            user_counter (int, optional): Number of users. Defaults to None.

        Raises:
            ValueError: If user_counter is None.
        """
        if user_counter is None:
            raise ValueError("user_counter cannot be none.")
        self.user_counter = user_counter

    def get_random_account_existence(self):
        """
        Get a random boolean representing the existence of a user account.

        Returns:
            bool: True if the user account exists, False otherwise.
        """
        # Weighted choices to simulate new user account creation
        new_user_choice_weight = [0.0, 0.1] if self.user_counter < UserCount.new_user_account_limit else [0.8, 0.2]
        return random.choices([True, False], weights=new_user_choice_weight)[0]

class RandNewAccountAttr:
    def __init__(self):
        """
        Initialize the RandNewAccountAttr object.
        """
        pass

    def generate_new_account_attributes(self):
        """
        Generate new attributes for a user account.

        Returns:
            dict: Dictionary containing new account attributes.
        """
        # Randomly select billing cycle, payment method, and device type
        self.billing_cycle = random.choices(
            [BillingType.monthly, BillingType.yearly], weights=[0.7, 0.3])[0]
        self.payment_method = random.choices(
            [PaymentType.credit, PaymentType.debit, PaymentType.checking],
            weights=[0.3, 0.3, 0.4])[0]
        self.device_type = random.choices(
            [DeviceType.tablet, DeviceType.tv, DeviceType.computer],
            weights=[0.1, 0.4, 0.5])[0]

        # Return dictionary containing new account attributes
        return {
            "billing_cycle": self.billing_cycle,
            "payment_method": self.payment_method,
            "device_type": self.device_type,
            "account_status": 'active'
        }


class RandExistsAccountAttr:
    def __init__(self, user_counter: int = None):
        """
        Initialize the RandExistsAccountAttr object.

        Args:
            user_counter (int, optional): Number of users. Defaults to None.

        Raises:
            ValueError: If user_counter is None.
        """
        if user_counter is None:
            raise ValueError("user_counter cannot be none.")
        self.user_counter = user_counter

    def generate_account_status(self):
        """
        Generate the status for an existing user account.

        Returns:
            AccountStatus: Status of the user account.
        """
        # Setup conditions here for paused, cancelled, and active accounts.
        account_status_weight = (
            [0.1, 0.1, 0.8]
            if 0 < self.user_counter < UserCount.active_user_account_limit
            else [0.2, 0.3, 0.5]
        )
        return random.choices(
            [
                AccountStatus.cancelled,
                AccountStatus.paused,
                AccountStatus.active
            ],
            weights=account_status_weight
        )

class RandLanguage:
    @classmethod
    def random_country_lang(cls, country_name):
        country_languages =  {
                'argentina': 'spanish',
                'australia': 'english',
                'austria': 'german',
                'bangladesh': 'bangla',
                'bolivia': 'spanish',
                'brazil': 'portuguese',
                'canada': ['english', 'french'],
                'chile': 'spanish',
                'ecuador': 'spanish',
                'egypt': 'arabic',
                'france': 'french',
                'germany': 'german',
                'greece': 'greek',
                'hungary': 'hungarian',
                'india': ['hindi', 'english', 'tamil', 'telegu', 'malayam'],
                'indonesia': 'indonesian',
                'ireland': ['english', 'irish'],
                'israel': 'hebrew',
                'italy': 'italian',
                'japan': 'japanese',
                'kuwait': 'arabic',
                'lebanon': 'arabic',
                'malaysia': 'malay',
                'mexico': 'spanish',
                'morocco': 'arabic',
                'netherlands': 'dutch',
                'new zealand': 'english',
                'nigeria': 'english',
                'oman': 'arabic',
                'pakistan': ['urdu', 'english'],
                'panama': 'spanish',
                'paraguay': ['spanish', 'guarani'],
                'peru': 'spanish',
                'poland': 'polish',
                'portugal': 'portuguese',
                'puerto rico': ['spanish', 'english'],
                'russia': 'russian',
                'saudi arabia': 'arabic',
                'south africa': ['afrikaans', 'english'],
                'south korea': 'korean',
                'spain': 'spanish',
                'sweden': 'swedish',
                'switzerland': ['german', 'french', 'italian'],
                'turkey': 'turkish',
    'united arab emirates': 'arabic',
    'united kingdom': 'english',
    'united states': 'english',
    'uruguay': 'spanish',
    'venezuela': 'spanish',
    'zimbabwe': 'english'
}

        language = country_languages[country_name]
        if isinstance(language, list):
            return random.choice(language)

        return language


if __name__ == "__main__":
    user_counter = 0
    # Usage
    # for i in range(200):
    #     user_counter += 1
    #     a = RandCountry(user_counter)
    #     print(a.get_random_country())
    # for i in range(200):
    #     user_counter += 1
    #     b = RandAccountExistence(user_counter)
    #     print(b.get_random_account_existence())
    # for i in range(200):
    #     user_counter +=1
    #     c = RandNewAccountAttr()
    #     print(c.generate_new_account_attributes())
    # print(user_counter) # 600

    print(RandLanguage.random_country_lang('india'))

