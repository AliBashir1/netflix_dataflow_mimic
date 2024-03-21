from enum import Enum


class GenderEnum(str, Enum):
    male: str = "m"
    female: str = "f"
    x: str = "x"


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


from enum import Enum


class UserIDRange(int, Enum):
    min: int = 1001
    max: str = 301024


class QueryLimit(int, Enum):
    min: int = 1
    max: int = 10
