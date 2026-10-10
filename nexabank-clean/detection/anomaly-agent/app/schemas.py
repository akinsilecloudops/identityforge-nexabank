
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.timeutil import to_utc

ID_PATTERN = r"^[A-Za-z0-9_-]{1,64}$"
REGION_PATTERN = r"^[A-Za-z][A-Za-z ]{0,39}$"
DN_PATTERN = r"^[A-Za-z0-9=,._ -]{1,256}$"


class Event(BaseModel):
    event_time: datetime
    event_type: Literal["transaction"]

    agent_id: str = Field(pattern=ID_PATTERN)
    assigned_region: str = Field(pattern=REGION_PATTERN)
    region: str = Field(pattern=REGION_PATTERN)
    device_id: str = Field(pattern=ID_PATTERN)
    cert_dn: str = Field(pattern=DN_PATTERN)

    amount: float = Field(ge=0, le=1_000_000_000_000)
    result: Literal["success", "failure"]

    @field_validator("event_time")
    @classmethod
    def _force_utc(cls, value: datetime) -> datetime:
        return to_utc(value)