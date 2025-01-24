from dataclasses import dataclass

from app.domain.specifications.coop_specifications import IsCapacityLessThen
from app.exceptions import IncorrectValueError


@dataclass(frozen=True)
class CoopDTO:
    name: str
    capacity: int

    @staticmethod
    def is_update_legal(update_coop_dto: "UpdateCoopDTO") -> bool:
        if (
                update_coop_dto.capacity and
                IsCapacityLessThen().is_satisfied_by(update_coop_dto, 0)
        ):
            raise IncorrectValueError(f"Вместимость курятника положительна")
        return True

    def __post_init__(self):
        self.__validate_capacity()

    def __validate_capacity(self):
        if IsCapacityLessThen().is_satisfied_by(self, 0):
            raise IncorrectValueError(f"Вместимость курятника положительна")


@dataclass(frozen=True)
class UpdateCoopDTO(CoopDTO):
    name: str | None = None
    capacity: int | None = None

    def __post_init__(self):
        pass