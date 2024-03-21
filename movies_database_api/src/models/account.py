from pydantic import BaseModel, Field
from typing_extensions import Annotated
from movies_database_api.src.models.commons import PaymentType, AccountStatus, BillingType, DeviceType
from movies_database_api.src.models.commons import UserIDRange, QueryLimit

class AccountCreateModel(BaseModel):
    user_id: Annotated[int, Field(ge=UserIDRange.min, le=UserIDRange.max)]
    payment_method: Annotated[PaymentType, Field(default=PaymentType.checking)]
    billing_cycle: Annotated[BillingType, Field(default=BillingType.monthly)]
    account_status: Annotated[AccountStatus, Field(default=AccountStatus.active)]
    device_type: Annotated[DeviceType, Field(default=DeviceType.tv)]

    class Config:
        validate_assignment = True


class AccountOut(BaseModel):
    user_id: int
    account_status: AccountStatus


class AccountStatusModel(BaseModel):
    user_id:Annotated[int, Field(ge=UserIDRange.min, le=UserIDRange.max)]
    account_status: AccountStatus