class Account:
    def __init__(self,
                 user_id: int,
                 payment_method: str ,
                 billing_cycle: str,
                 device_type: str,
                account_status: str ='active'
                 ) -> None:
        self.user_id = user_id
        self.payment_method = payment_method
        self.billing_cycle = billing_cycle
        self.device_type = device_type
        self.account_status = account_status


    def create_account(self):
        pass

    def cancel_account(self):
        pass

    def pause_account(self):
        pass

class AccountOut:
    pass
