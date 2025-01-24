from app.domain.specifications.bird_specifications import (
    IsBroiler, IsHavesAvgEggsPerMonth, IsWeightLessThen)
from app.exceptions import IncorrectValueError

from dataclasses import dataclass
from enum import Enum


class BirdTypeEnum(Enum):
    LAYING_HEN = "Несушка"
    BROILER = "Бройлер"


@dataclass(frozen=True)
class BirdDTO:
    name: str
    type: str
    weight: int
    coop_oid: str
    avg_eggs_per_month: int | None = None

    def is_update_legal(self, update_bird_dto: "UpdateBirdDTO") -> bool:
        if update_bird_dto.avg_eggs_per_month:
            if IsBroiler().is_satisfied_by(self):
                raise IncorrectValueError(
                    "Нельзя обновлять среднее кол-во яиц для бройлера")

        if update_bird_dto.type:
            raise IncorrectValueError("Изменение типа птицы запрещено")
        return True

    def __post_init__(self):
        self.__validate_bird_type_enum()
        self.__validate_avg_eggs_per_month()
        self._validate_weight()

    def __validate_bird_type_enum(self):
        bird_type_values = [bird_type.value for bird_type in BirdTypeEnum]
        if self.type not in bird_type_values:
            raise IncorrectValueError(
                f"Тип птицы должен быть из списка: {bird_type_values}")

    def __validate_avg_eggs_per_month(self) -> None:
        if (
                IsBroiler().is_satisfied_by(self) and
                IsHavesAvgEggsPerMonth().is_satisfied_by(self)
        ):
            raise IncorrectValueError(
                "Нельзя добавить к бройлеру среднее кол-во яиц")

    def _validate_weight(self):
        if (
                self.weight and
                IsWeightLessThen().is_satisfied_by(self, 0)
        ):
            raise IncorrectValueError("Вес не может быть отрицательным")


@dataclass(frozen=True)
class UpdateBirdDTO(BirdDTO):
    name: str | None = None
    type: str | None = None
    weight: int | None = None
    coop_oid: str | None = None
    avg_eggs_per_month: int | None = None

    def __post_init__(self):
        self._validate_weight()
