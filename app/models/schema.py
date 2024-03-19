from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing_extensions import NotRequired, TypedDict


class LeadSchema(TypedDict):
    name: str
    signal: list[int]
    sample_count: NotRequired[int]


class ECGSchema(BaseModel):
    id: int
    date: datetime
    leads: list[LeadSchema]

    model_config = ConfigDict(from_attributes=True)
