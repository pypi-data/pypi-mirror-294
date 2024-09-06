import enum


class ActivityEventType(enum.StrEnum):
    LAST_LOGIN = "LastLogin"
    LAST_ACTIVITY = "LastActivity"


class CustomAttributeType(enum.StrEnum):
    STRING = "STRING"
    USER = "USER"


class CustomAttributeCustomizedType(enum.StrEnum):
    ACCOUNT = "ACCOUNT"
    ENTITLEMENMT = "ENTITLEMENT"
    RESOURCE = "RESOURCE"
