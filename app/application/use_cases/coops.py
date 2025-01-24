from typing import Sequence

from app.domain.value_objects.coops import CoopStatistic
from app.exceptions import EmptyDataError, NotFoundError
from app.infrastructure.models.coops import Coop
from app.application.use_cases.base import IUseCase
from app.domain.entities.coops import CoopDTO, UpdateCoopDTO
from app.infrastructure.repositories.coops import BaseCoopRepository


class GetCoopsUseCase(IUseCase):
    def __init__(self, coop_repo: BaseCoopRepository) -> None:
        self.__coop_repo = coop_repo

    def execute(self) -> Sequence[CoopDTO]:
        coops = self.__coop_repo.get()
        return coops


class CreateCoopUseCase(IUseCase):
    def __init__(self, coop_repo: BaseCoopRepository) -> None:
        self.__coop_repo = coop_repo

    def execute(self, coop_dto: CoopDTO) -> Coop:
        coop = Coop.from_dto(coop_dto)
        self.__coop_repo.save(coop)
        return coop


class DeleteCoopUseCase(IUseCase):
    def __init__(self, coop_repo: BaseCoopRepository) -> None:
        self.__coop_repo = coop_repo

    def execute(self, coop_oid: str) -> None:
        coop = self.__coop_repo.get_by_oid(coop_oid)
        if not coop:
            raise NotFoundError(f"Coop with oid {coop_oid} not found")
        self.__coop_repo.delete(coop_oid)
        self.__coop_repo.save()


class UpdateCoopUseCase(IUseCase):
    def __init__(self, coop_repo: BaseCoopRepository) -> None:
        self.__coop_repo = coop_repo

    def execute(
            self,
            coop_oid: str,
            update_coop_dto: UpdateCoopDTO
    ) -> Coop | None:
        coop = self.__coop_repo.get_by_oid(coop_oid)
        if not coop:
            raise NotFoundError(f"Курятник с oid {coop_oid} не найден")
        coop_dto = coop.to_dto()
        if coop_dto.is_update_legal(update_coop_dto):
            updated_coop: Coop = self.__coop_repo.update_by_oid(
                coop_oid, update_coop_dto)
            if not updated_coop:
                raise EmptyDataError(
                    f"Пустые данные для обновления курятника с oid {coop_oid}")
            self.__coop_repo.save()
            return updated_coop


class GetCoopStatisticUseCase(IUseCase):
    def __init__(self, coop_repo: BaseCoopRepository) -> None:
        self.__coop_repo = coop_repo

    def execute(self, coop_oid: str) -> CoopStatistic:
        avg_eggs = round(
            self.__coop_repo.get_birds_avg_eggs_per_month_by_coop_oid(
                coop_oid
            ) or 0
        )
        avg_weight = round(
            self.__coop_repo.get_avg_weight_by_coop_oid(coop_oid) or 0)
        return CoopStatistic(
            avg_eggs_per_month=avg_eggs, avg_weight=avg_weight)

