from app.domain.specifications.base import Specification


class IsCapacityLessThen(Specification):
    def is_satisfied_by(
            self,
            candidate: "CoopDTO", # noqa
            capacity_value: int
    ) -> bool:
        return int(candidate.capacity) < capacity_value
