from datetime import datetime

from pydantic import BaseModel

from app.models import ECGSchema, LeadSchema


class CreateECGRequest(BaseModel):
    id: str
    date: datetime
    leads: list[LeadSchema]


class CreateECGResponse(ECGSchema):
    pass


class ReadECGResponse(ECGSchema):
    pass


class ReadAllECGResponse(BaseModel):
    ecgs: list[ECGSchema]
