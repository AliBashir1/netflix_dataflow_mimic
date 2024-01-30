from movies_database_api.src.models.account import AccountCreateModel
from movies_database_api.src.models.commons import AccountStatus, BillingType
from movies_database_api.src.crud.commons import update_insert_query_executor, select_query_executor
from typing import Union
from typing_extensions import Annotated
import datetime as dt
from datetime import date
import pytz
from dateutil.relativedelta import relativedelta


def get_today_date() -> date:
    ny_timezone = pytz.timezone("america/new_york")
    today_date = ny_timezone.localize(dt.datetime.now())
    return today_date


@update_insert_query_executor
async def create_account(new_account: AccountCreateModel) -> Union[bool, str]:
    date_format = "%Y-%m-%d"
    billing_due_date: str = '1900-01-01'
    today_date = get_today_date()
    start_date: str = today_date.strftime(date_format)

    if new_account.billing_cycle == BillingType.monthly:
        billing_due_date = (today_date + relativedelta(months=1)).strftime(date_format)
    elif new_account.billing_cycle == BillingType.yearly:
        billing_due_date = (today_date + relativedelta(years=1)).strftime(date_format)

    # create account and set does_account_exists to True in users table.
    q = """
        INSERT INTO accounts(
                        user_id, 
                        created_at, 
                        bill_due_date, 
                        payment_method, 
                        billing_cycle, 
                        account_status,
                        device_type
                        )
                VALUES(
                        {},
                        '{}',
                        '{}',
                        '{}',
                        '{}',
                        '{}',
                        '{}'
                        );

            UPDATE users set does_account_exists = True 
            WHERE id = {};
        
                        """.format(new_account.user_id,
                                   start_date,
                                   billing_due_date,
                                   new_account.payment_method,
                                   new_account.billing_cycle,
                                   AccountStatus.active,
                                   new_account.device_type,
                                   new_account.user_id)
    return q


@update_insert_query_executor
async def pause_account(user_id: int, new_account_status: AccountStatus) -> Union[bool, str]:
    update_account_status_query = """
        CALL update_account_status(user_id_in := {},new_account_status := '{}'::account_status);
        """.format(user_id, new_account_status)
    return update_account_status_query


@select_query_executor(return_model_type='account')
async def get_random_account(account_status: AccountStatus = 'active', number_of_accounts: int = 1) -> str:
    q = """
        SELECT 
            user_id,
            account_status
        FROM accounts
        WHERE account_status = '{}'
        ORDER BY random()
        LIMIT {};
             
    """.format(account_status, number_of_accounts)
    return q


@select_query_executor(return_model_type='account')
async def get_account_by_user_id(user_id: int, account_status: AccountStatus = AccountStatus.active):
    q = """
        SELECT
            user_id, 
            account_status
        FROM accounts
        WHERE user_id = {} and account_status = '{}';
    """.format(user_id, account_status)
    return q


@select_query_executor(return_model_type='account')
async def get_random_account_by_country(country: str, account_status: AccountStatus = 'active',
                                        number_of_accounts: int = 1) -> str:
    q = """
        SELECT 
            a.user_id,
            a.account_status
        FROM accounts a
        JOIN users u ON a.user_id = u.id
        WHERE a.account_status = '{}' and u.country = '{}'
        ORDER BY random()
        LIMIT {};

    """.format(account_status, country, number_of_accounts)
    return q
