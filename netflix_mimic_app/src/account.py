import requests
import json
from netflix_mimic_app.src.utilities.api_key import get_api_key
from netflix_mimic_app.src.commons import AccountStatus, DeviceType, BillingType, PaymentType
from netflix_mimic_app.src.commons import send_request

BASEURL: str = 'http://movies_database_api:8000'
KEY = get_api_key()


class NewAccount:
    """A class representing a new user account."""

    def __init__(
            self,
            user_id: int,
            payment_method: PaymentType,
            billing_cycle: BillingType,
            device_type: DeviceType,
            account_status: AccountStatus
    ) -> None:
        """
        Initialize the NewAccount object.

        Parameters:
            user_id: int
                The ID of the user.
            payment_method: str
                The method of payment for the account.
            billing_cycle: str
                The billing cycle for the account.
            device_type: str
                The type of device associated with the account.
            account_status: str, optional (default='active')
                The status of the account. Defaults to 'active'.
        """
        self.user_id = user_id
        self.payment_method = payment_method
        self.billing_cycle = billing_cycle
        self.device_type = device_type
        self.account_status = account_status

    # A decorated with request sending functionality
    @send_request(request_type='post-data')
    def create_account(self):
        """
        Create the account.

        Returns:
            tuple: A tuple containing the relative URL and the data to be sent in the request.
        """
        rel_url = "/accounts/create_account"
        data = {**self.__dict__}
        return rel_url, data


class SetAccountStatus:
    """A class to set the status of an account."""

    def __init__(
            self,
            user_id,
            account_status: AccountStatus
    ) -> None:
        """
        Initialize the SetAccountStatus object.

        Parameters:
            user_id: int
                The ID of the user whose account status will be set.
            account_status: AccountStatus EnumType
                The new status to set for the account.
        """
        self.user_id = user_id
        self.account_status = account_status

    # A decorated with request sending functionality
    @send_request(request_type="post-data")
    def set_status(self):
        """
        Set the status of the account.

        Returns:
            tuple: A tuple containing the relative URL and the data to be sent in the request.
        """
        rel_url = "/accounts/set_account_status/"
        data = {**self.__dict__}
        return rel_url, data


if __name__ == "__main__":
    from netflix_mimic_app.src.randomize_attributes import RandNewAccountAttributes

    # new account
    new_account_attr = RandNewAccountAttributes.generate_new_account_attributes()
    new_account_attr["user_id"] = 1002
    print(new_account_attr)
    new_account = NewAccount(**new_account_attr)
    new_account.create_account()
    # existing_account = SetAccountStatus(1001, AccountStatus.cancelled)
    # existing_account.set_status()
