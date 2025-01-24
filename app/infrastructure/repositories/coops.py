from typing import Generic, Any

from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain.entities.birds import BirdTypeEnum
from app.infrastructure.models.birds import Bird
from app.exceptions import NotFoundError, DatabaseError
from app.infrastructure.models.coops import Coop
from app.infrastructure.repositories.base import BaseRepository, T
from app.logger import Logger


class BaseCoopRepository(BaseRepository, Generic[T]):
    def __init__(self, db: Session, model: Any):
        super().__init__(db, model)

    def delete(self, coop_oid: str) -> None:
        raise NotImplementedError()

    def get_birds_avg_eggs_per_month_by_coop_oid(
            self,
            coop_oid: str
    ) -> float | None:
        raise NotImplementedError()

    def get_avg_weight_by_coop_oid(self, coop_oid: str) -> float | None:
        raise NotImplementedError()


class CoopRepository(BaseCoopRepository[Coop]):
    def __init__(self, db: Session):
        super().__init__(db, Coop)

    def delete(self, coop_oid: str) -> None:
        coop = self.get_by_oid(coop_oid)
        if not coop:
            raise NotFoundError(f"Coop with oid {coop_oid} not found")
        self._db.delete(coop)

    def get_birds_avg_eggs_per_month_by_coop_oid(
            self,
            coop_oid: str
    ) -> float | None:
        try:
            stmt = (
                select(func.avg(Bird.avg_eggs_per_month))
                .where(Bird.coop_oid == coop_oid)
                .where(Bird.type == BirdTypeEnum.LAYING_HEN.value)
            )

            result = self._db.execute(stmt)
            avg_eggs_per_month = result.scalar()
            if not avg_eggs_per_month:
                return None
            return avg_eggs_per_month
        except SQLAlchemyError as e:
            logger_text = (
                f"Failed to get birds avg eggs per month by coop oid: {e}")
            Logger.error(logger_text)
            raise DatabaseError()

    def get_avg_weight_by_coop_oid(self, coop_oid: str) -> float | None:
        try:
            stmt = (
                select(func.avg(Bird.weight))
                .where(Bird.coop_oid == coop_oid)
                .where(Bird.type == BirdTypeEnum.BROILER.value)
            )

            result = self._db.execute(stmt)
            avg_weight = result.scalar()
            if not avg_weight:
                return None
            return avg_weight
        except SQLAlchemyError as e:
            logger_text = f"Failed to get birds avg weight by coop oid: {e}"
            Logger.error(logger_text)
            raise DatabaseError()
