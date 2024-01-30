from enum import Enum


class GenderEnum(str, Enum):
    male: str = "m"
    female: str = "f"
    x: str = "x"


class AccountStatus(str, Enum):
    active: str = "active"
    pause: str = "paused"
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
