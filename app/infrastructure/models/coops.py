from copy import deepcopy
from dataclasses import asdict
from uuid import uuid4

from app.domain.entities.coops import CoopDTO
from app.infrastructure.database.base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String


class Coop(Base):
    __tablename__ = "coops"

    oid: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    name: Mapped[str] = mapped_column(String(32), index=True)
    capacity: Mapped[int]

    birds: Mapped[list["Bird"]] = relationship(
        uselist=True, back_populates="coop")

    @staticmethod
    def from_dto(coop_dto: CoopDTO) -> "Coop":
        coop = Coop(**asdict(coop_dto))
        return coop

    def to_dto(self) -> CoopDTO:
        bird_dict = deepcopy(self.__dict__)
        del bird_dict["_sa_instance_state"]
        del bird_dict["oid"]
        bird_dto = CoopDTO(**bird_dict)
        return bird_dto
