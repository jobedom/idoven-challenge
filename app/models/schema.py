from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .lead import Lead


class ECGSchema(BaseModel):
    id: int
    date: datetime
    leads: list[Lead]

    model_config = ConfigDict(from_attributes=True)
