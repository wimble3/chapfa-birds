from app.domain.specifications.base import Specification


class IsBroiler(Specification):
    def is_satisfied_by(self, candidate: "BirdDTO") -> bool:  # noqa
        from app.domain.entities.birds import BirdTypeEnum
        return candidate.type == BirdTypeEnum.BROILER.value


class IsHavesAvgEggsPerMonth(Specification):
    def is_satisfied_by(self, candidate: "BirdDTO") -> bool:  # noqa
        return bool(candidate.avg_eggs_per_month)


class IsWeightLessThen(Specification):
    def is_satisfied_by(
            self,
            candidate: "BirdDTO", # noqa
            weight_value: int
    ) -> bool:
        return int(candidate.weight) < weight_value
