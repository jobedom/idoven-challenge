from typing import Union

from pydantic import BaseModel
from typing_extensions import TypedDict

from .insight_positive_count import PositiveCountInsightSchema
from .insight_zero_crossings import ZeroCrossingsInsightSchema

AnyInsightSchema = Union[ZeroCrossingsInsightSchema, PositiveCountInsightSchema]


class LeadInsights(TypedDict):
    lead: str
    insights: list[AnyInsightSchema]


class ECGInsightsResponse(BaseModel):
    ecg_insights: list[LeadInsights]
