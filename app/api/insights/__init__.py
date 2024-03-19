from .insight_positive_count import calculate as calculate_positive_count_insight
from .insight_zero_crossings import calculate as calculate_zero_crossings_insight

insight_calculators = [
    calculate_zero_crossings_insight,
    calculate_positive_count_insight,
]


def calculate_insights(lead):
    return [calculator(lead) for calculator in insight_calculators]
