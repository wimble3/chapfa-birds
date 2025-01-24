from dataclasses import dataclass, asdict
from typing import Type, TypeVar, Sequence, Generic
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from abc import ABC, abstractmethod

from app.exceptions import DatabaseError
from app.infrastructure.database.base import Base
from app.infrastructure.dtos.pagination_dto import PaginationDTO
from app.logger import Logger


T = TypeVar("T", bound=Base)


class IRepository(ABC, Generic[T]):
    @abstractmethod
    def get(
        self,
        pagination_data: PaginationDTO | None = None
    ) -> Sequence[T] | bool | None:
        pass

    @abstractmethod
    def get_by_oid(self, oid: str) -> T | None:
        pass

    @abstractmethod
    def update_by_oid(self, oid: str, update_dto: dataclass) -> T | None:
        pass

    @abstractmethod
    def save_all(self, objs: Sequence[object]) -> None:
        pass

    @abstractmethod
    def save(self, obj: object | None = None) -> None:
        pass

    @abstractmethod
    def delete(self, *args) -> None:
        pass


class BaseRepository(IRepository[T], Generic[T]):
    def __init__(self, db: Session, model: Type[T] | None = None):
        self._db = db
        self._model = model

    def get(
        self,
        pagination_dto: PaginationDTO | None = None
    ) -> Sequence[T] | bool | None:
        try:
            stmt = select(self._model)
            if not pagination_dto:
                return self._db.scalars(stmt).all()

            limit = pagination_dto.limit
            if limit:
                stmt.limit(limit)
            offset = pagination_dto.offset
            if offset:
                stmt.offset(offset)
            return self._db.scalars(stmt).all()
        except SQLAlchemyError as e:
            logger_text = (
                f"Failed to get from table {self._model.__tablename__}: {e}")
            Logger.error(logger_text)
            raise DatabaseError()

    def get_by_oid(self, oid: str) -> T | None:
        try:
            stmt = (
                select(self._model)
                .where(self._model.oid == oid)
            )
            return self._db.scalar(stmt)
        except SQLAlchemyError as e:
            logger_text = (
                f"Failed to get by id from table "
                f"{self._model.__tablename__}: {e}")
            Logger.error(logger_text)
            raise DatabaseError()

    def update(self, obj: T, update_data: dataclass) -> T:
        try:
            update_data = {
                key: value for key, value in asdict(update_data).items()
                if value is not None
            }

            for key, value in update_data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            self._db.add(obj)
            self._db.flush()
            return obj
        except SQLAlchemyError as e:
            logger_text = (
                f"Failed to update object {obj} in table "
                f"{self._model.__tablename__}: {e}"
            )
            Logger.error(logger_text)
            raise DatabaseError()

    def update_by_oid(self, oid: str, update_dto: dataclass) -> T | None:
        try:
            update_data = {
                key: value for key, value in asdict(update_dto).items()
                if value is not None
            }
            if not update_data:
                return None

            stmt = (
                update(self._model)
                .where(self._model.oid == oid)
                .values(**update_data)
                .returning(self._model)
            )
            result = self._db.execute(stmt).scalar_one_or_none()
            self._db.flush()
            return result
        except SQLAlchemyError as e:
            logger_text = (
                f"Failed to update {self._model.__tablename__} with id {oid}: "
                f"{e}"
            )
            Logger.error(logger_text)
            raise DatabaseError()

    def save_all(self, objs: Sequence[object]) -> None:
        try:
            self._db.add_all(objs)
            self._db.commit()
            self._db.close()
        except SQLAlchemyError as e:
            logger_text = f"Failed to save objects {objs}: {e}"
            Logger.error(logger_text)
            raise DatabaseError()

    def save(self, obj: object | None = None) -> None:
        try:
            if obj:
                self._db.add(obj)
            self._db.commit()
            self._db.close()
        except SQLAlchemyError as e:
            logger_text = f"Failed to save object {obj}: {e}"
            Logger.error(logger_text)
            raise DatabaseError()

    def delete(self, *args) -> None:
        raise NotImplementedError()
