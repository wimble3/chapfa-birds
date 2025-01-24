from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings import Settings


engine = create_engine(url=Settings.SQLALCHEMY_DATABASE_URI)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    @staticmethod
    def from_dto(*args, **kwargs) -> Any:
        raise NotImplementedError()

    def to_dto(self, *args, **kwargs) -> Any:
        raise NotImplementedError()
