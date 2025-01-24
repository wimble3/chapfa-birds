from dataclasses import dataclass


@dataclass(frozen=True)
class CoopStatistic:
    avg_eggs_per_month: int
    avg_weight: int
