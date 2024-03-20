from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing_extensions import NotRequired, TypedDict


class UserSchema(BaseModel):
    id: int
    email: str
    password: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class LeadSchema(TypedDict):
    name: str
    signal: list[int]
    sample_count: NotRequired[int]


class ECGSchema(BaseModel):
    id: str
    owner_id: int
    date: datetime
    leads: list[LeadSchema]

    model_config = ConfigDict(from_attributes=True)
