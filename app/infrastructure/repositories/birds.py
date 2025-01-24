from math import ceil
from typing import Generic, Any, Sequence

from sqlalchemy import select, func, asc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.exceptions import DatabaseError
from app.infrastructure.dtos.pagination_dto import PaginationDTO
from app.infrastructure.models.birds import Bird
from app.infrastructure.repositories.base import BaseRepository, T
from app.logger import Logger


class BaseBirdRepository(BaseRepository, Generic[T]):
    def __init__(self, db: Session, model: Any):
        super().__init__(db, model)

    def get_by_coop_oid(
            self,
            coop_oid: str,
            pagination_dto: PaginationDTO
    ) -> Sequence[Bird]:
        raise NotImplementedError()

    def get_total_pages_by_coop_oid(
            self,
            coop_oid: str,
            pagination_dto: PaginationDTO
    ) -> int:
        raise NotImplementedError()

    def delete(self, bird_oid: str) -> None:
        raise NotImplementedError()


class BirdRepository(BaseBirdRepository[Bird]):
    def __init__(self, db: Session):
        super().__init__(db, Bird)

    def get_by_coop_oid(
            self,
            coop_oid: str,
            pagination_dto: PaginationDTO
    ) -> Sequence[Bird]:
        try:
            stmt = (
                select(Bird)
                .where(Bird.coop_oid == coop_oid)
            )
            if pagination_dto:
                stmt = (
                    stmt.limit(
                        pagination_dto.limit
                    ).offset(
                        pagination_dto.offset
                    )
                )
            stmt = stmt.order_by(asc(Bird.name))
            result = self._db.execute(stmt)
            birds = result.scalars().all()
            return birds
        except SQLAlchemyError as e:
            logger_text = f"Failed to get birds by coop_id: {e}"
            Logger.error(logger_text)
            raise DatabaseError()

    def get_total_pages_by_coop_oid(
            self,
            coop_oid: str,
            pagination_dto: PaginationDTO
    ) -> int:
        try:
            stmt = (
                select(func.count())
                .select_from(Bird)
                .where(Bird.coop_oid == coop_oid)
            )
            total_birds = self._db.execute(stmt).scalar()

            if total_birds is None or pagination_dto.limit == 0:
                return 0

            total_pages = ceil(total_birds / pagination_dto.limit)
            return total_pages
        except SQLAlchemyError as e:
            logger_text = (
                f"Failed to get total pages by coop_oid {coop_oid}: {e}")
            Logger.error(logger_text)
            raise DatabaseError()

    def delete(self, bird_oid: str) -> None:
        bird = self.get_by_oid(bird_oid)
        self._db.delete(bird)
