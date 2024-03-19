from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LeadSchema(BaseModel):
    id: int
    ecg_id: int
    name: str
    signal: list[int]

    model_config = ConfigDict(from_attributes=True)


class ECGSchema(BaseModel):
    id: int
    date: datetime
    leads: list[LeadSchema]

    model_config = ConfigDict(from_attributes=True)
