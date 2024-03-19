from app.models.lead import Lead

from .insight_zero_crossings import calculate as calculate_zero_crossings_insight
from .schema import AnyInsightSchema

insight_calculators = [
    calculate_zero_crossings_insight,
]


def calculate_insights(lead: Lead) -> list[AnyInsightSchema]:
    return [calculator(lead) for calculator in insight_calculators]
