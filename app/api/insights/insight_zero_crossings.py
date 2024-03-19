from typing_extensions import TypedDict

from app.models import LeadSchema


class ZeroCrossingsInsightSchema(TypedDict):
    zero_crossings: int


def calculate(lead: LeadSchema) -> ZeroCrossingsInsightSchema:
    sequence = lead["signal"]
    zero_crossings = sum((a ^ b) < 0 for a, b in zip([sequence[0]] + sequence, sequence))
    return {"zero_crossings": zero_crossings}
