from typing_extensions import TypedDict

from app.models.lead import Lead


class PositiveCountInsightSchema(TypedDict):
    positive_count: int


def calculate(lead: Lead) -> PositiveCountInsightSchema:
    sequence = lead["signal"]
    positive_count = sum(1 if value >= 0 else 0 for value in sequence)
    return {"positive_count": positive_count}
