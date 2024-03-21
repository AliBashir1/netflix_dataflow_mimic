from enum import Enum
import requests
import json

from netflix_mimic_app.src.utilities.api_key import get_api_key

class UserCount(int, Enum):
    new_user_account_limit: int = 2000 # new accounts
    user_limit: int = 25000 # overall user limit
    active_user_perc: int = 90
    active_user_account_limit = 15000 # activa users before account pause or cancellation start

class AccountStatus(str, Enum):
    active: str = "active"
    paused: str = "paused"
    cancelled: str = "cancelled"


class PaymentType(str, Enum):
    credit: str = "credit"
    debit: str = "debit"
    checking: str = "checking"


class BillingType(str, Enum):
    monthly: str = "monthly"
    yearly: str = "yearly"


class DeviceType(str, Enum):
    tv: str = "tv"
    tablet: str = "tablet"
    computer: str = "computer"


# decorators for requests method


def send_request(request_type: str = 'get'):
    """
    A decorator function to handle HTTP requests.

    Parameters:
        request_type: str, optional (default='get')
            The type of HTTP request to be made. Supported types: 'get', 'post', 'delete', 'post-data'.

    Returns:
        function: A wrapper function based on the specified request type.

    Raises:
        ValueError: If the specified request type is not supported.
    """
    BASEURL: str = 'http://movies_database_api:8000'
    KEY: str = get_api_key()
    headers = {
        "x-access-token": KEY,
        "Content-type": "application/json",
    }

    def send(func):
        """
        Inner function to handle different HTTP request types.

        Parameters:
            func: The function to be wrapped.

        Returns:
            function: A wrapper function based on the specified request type.
        """
        def post_wrapper(*args, **kwargs):
            """
            Wrapper function for sending POST requests.

            Parameters:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                dict: The JSON response if the request is successful.

            Raises:
                ValueError: If the request fails.
            """
            url = func(*args, **kwargs)
            res = requests.post(
                BASEURL + url,  # full url
                headers=headers
            )
            if res.status_code == 200:
                return res.json()
            else:
                raise ValueError("Error: {}".format(res.json()))

        def post_data_wrapper(*args, **kwargs):
            """
            Wrapper function for sending POST requests with data.

            Parameters:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                dict: The JSON response if the request is successful.

            Raises:
                ValueError: If the request fails.
            """
            url, data = func(*args, **kwargs)
            res = requests.post(
                BASEURL + url,
                headers=headers,
                data=json.dumps(data)
            )

            if res.status_code == 200:
                return res.json()
            else:
                raise ValueError("Error: {}".format(res.json()))

        def get_wrapper(*args, **kwargs):
            """
            Wrapper function for sending GET requests.

            Parameters:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                dict: The JSON response if the request is successful.

            Raises:
                ValueError: If the request fails.
            """
            url = func(*args, **kwargs)
            res = requests.get(
                BASEURL + url,  # full url
                headers=headers
            )
            print(url)

            if res.status_code == 200:
                return res.json()
            else:
                raise ValueError("Error: {}".format(res.json()))

        def delete_wrapper(*args, **kwargs):
            """
            Wrapper function for sending DELETE requests.

            Parameters:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                dict: The JSON response if the request is successful.

            Raises:
                ValueError: If the request fails.
            """
            url = func(*args, **kwargs)
            res = requests.delete(
                BASEURL + url,
                headers=headers
            )
            if res.status_code == 200:
                return res.json()
            else:
                raise ValueError("Error: {}".format(res.json()))

        # Return the appropriate wrapper function based on the request type
        if request_type == 'get':
            return get_wrapper
        elif request_type == 'post':
            return post_wrapper
        elif request_type == 'delete':
            return delete_wrapper
        elif request_type == 'post-data':
            return post_data_wrapper
        else:
            raise ValueError("Not implemented yet.")

    return send

