from enum import Enum

from debuff.services.interfaces import show_all_interface_names


class DirectionsEnum(str, Enum):
    outgoing = "outgoing"
    incoming = "incoming"
    bidirectional = "bidirectional"


class InterfaceStateEnum(str, Enum):
    up = "up"
    down = "down"

    #  Make enum case insensitive
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member == value.lower():
                return member


class TempEnum(str, Enum):
    pass


interface_enum_values = {x: x for x in show_all_interface_names()}
InterfaceEnum = TempEnum("InterfaceEnum", interface_enum_values)
