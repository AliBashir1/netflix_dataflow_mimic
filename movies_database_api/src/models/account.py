from pydantic import BaseModel, Field
from typing_extensions import Annotated
from movies_database_api.src.models.commons import PaymentType, AccountStatus, BillingType, DeviceType


class AccountCreateModel(BaseModel):
    user_id: Annotated[int, Field(ge=10001, le=499999)]
    payment_method: Annotated[PaymentType, Field(default=PaymentType.checking)]
    billing_cycle: Annotated[BillingType, Field(default=BillingType.monthly)]
    account_status: Annotated[AccountStatus, Field(default=AccountStatus.active)]
    device_type: Annotated[DeviceType, Field(default=DeviceType.tv)]

    class Config:
        validate_assignment = True


class AccountOut(BaseModel):
    user_id: int
    account_status: AccountStatus
