from typing import Union

from pydantic import BaseModel
from typing_extensions import TypedDict

from .insight_zero_crossings import ZeroCrossingsInsightSchema

AnyInsightSchema = Union[ZeroCrossingsInsightSchema]


class LeadInsights(TypedDict):
    lead: str
    insights: list[AnyInsightSchema]


class ECGInsightsResponse(BaseModel):
    ecg_insights: list[LeadInsights]
