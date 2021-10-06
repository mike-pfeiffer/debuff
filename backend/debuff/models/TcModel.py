from enum import Enum

from debuff.services.interfaces import show_all_interface_names
from pydantic import BaseModel, Field, validator


class Directions(str, Enum):
    outgoing = "outgoing"
    incoming = "incoming"
    bidirectional = "bidirectional"


class TcSetValues(BaseModel):
    interface: str = Field(...)
    direction: Directions = Field(...)
    delay: float = Field(0, ge=0)
    jitter: float = Field(0, ge=0)
    loss: float = Field(0, le=100, ge=0)

    class Config:
        use_enum_values = True

    @validator("interface", always=True)
    def validate_interface(cls, value):
        if value not in show_all_interface_names():
            raise ValueError(f"Interface {value} does not exist")
        else:
            return value
