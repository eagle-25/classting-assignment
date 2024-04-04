from enum import Enum


class UserType(str, Enum):
    SUBSCRIBER = "subscriber"
    PUBLISHER = "publisher"
