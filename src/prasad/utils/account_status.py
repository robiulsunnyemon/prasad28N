from enum import Enum


class AccountStatus(Enum):
    NOT_VERIFIED= "NOT_VARIFIED"
    PENDING="PENDING"
    ACTIVE="ACTIVE"
    SUSPENDED="SUSPENDED"