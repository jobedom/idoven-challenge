from pydantic import BaseModel

from app.models import LeadSchema


class CreateLeadRequest(BaseModel):
    ecg_id: int
    name: str
    signal: list[int]


class CreateLeadResponse(LeadSchema):
    pass


class ReadLeadResponse(LeadSchema):
    pass


class ReadAllLeadResponse(BaseModel):
    leads: list[LeadSchema]


class UpdateLeadRequest(BaseModel):
    ecg_id: int
    name: str
    signal: list[int]


class UpdateLeadResponse(LeadSchema):
    pass
