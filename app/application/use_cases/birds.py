from typing import Any, Sequence

from app.application.dtos.front_pagination_dto import FrontPaginationDTO
from app.exceptions import NotFoundError
from app.helpers.dto import DTOHelper
from app.infrastructure.models.birds import Bird
from app.domain.entities.birds import BirdDTO, UpdateBirdDTO
from app.application.use_cases.base import IUseCase
from app.infrastructure.repositories.birds import BaseBirdRepository


class CreateBirdUseCase(IUseCase):
    def __init__(self, bird_repo: BaseBirdRepository) -> None:
        self.__bird_repo = bird_repo

    def execute(self, bird_dto: BirdDTO) -> Any:
        bird = Bird.from_dto(bird_dto)
        self.__bird_repo.save(bird)


class GetBirdsByCoopUseCase(IUseCase):
    def __init__(self, bird_repo: BaseBirdRepository) -> None:
        self.__bird_repo = bird_repo

    def execute(
            self,
            coop_oid: str,
            front_pagination_dto: FrontPaginationDTO | None = None
    ) -> tuple[Sequence[Bird], int]:
        pagination_dto = DTOHelper.pagination_dto_from_front(
            front_pagination_dto)
        birds = self.__bird_repo.get_by_coop_oid(coop_oid, pagination_dto)
        total_pages = self.__bird_repo.get_total_pages_by_coop_oid(
            coop_oid, pagination_dto)
        return birds, total_pages


class DeleteBirdUseCase(IUseCase):
    def __init__(self, bird_repo: BaseBirdRepository) -> None:
        self.__bird_repo = bird_repo

    def execute(self, bird_oid: str) -> None:
        bird = self.__bird_repo.get_by_oid(bird_oid)
        if not bird:
            raise NotFoundError(f"Птица с oid {bird_oid} не найдена")
        self.__bird_repo.delete(bird_oid)
        self.__bird_repo.save()


class UpdateBirdUseCase(IUseCase):
    def __init__(self, bird_repo: BaseBirdRepository) -> None:
        self.__bird_repo = bird_repo

    def execute(
            self,
            bird_oid: str,
            update_bird_dto: UpdateBirdDTO
    ) -> Bird | None:
        bird: Bird = self.__bird_repo.get_by_oid(bird_oid)
        if not bird:
            raise NotFoundError(f"Птица с oid {bird_oid} не найдена")
        bird_dto = bird.to_dto()
        if bird_dto.is_update_legal(update_bird_dto):
            updated_bird = self.__bird_repo.update(bird, update_bird_dto)
            self.__bird_repo.save()
            return updated_bird
