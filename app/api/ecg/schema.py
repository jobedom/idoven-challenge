from datetime import datetime

from pydantic import BaseModel

from app.models import ECGSchema


class CreateECGRequest(BaseModel):
    date: datetime


class CreateECGResponse(ECGSchema):
    pass


class ReadECGResponse(ECGSchema):
    pass


class ReadAllECGResponse(BaseModel):
    ecgs: list[ECGSchema]


class UpdateECGRequest(BaseModel):
    date: datetime


class UpdateECGResponse(ECGSchema):
    pass
