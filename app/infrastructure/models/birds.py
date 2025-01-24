from copy import deepcopy
from dataclasses import asdict
from typing import Optional
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.birds import BirdDTO
from app.infrastructure.database.base import Base


class Bird(Base):
    __tablename__ = "birds"

    oid: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    name: Mapped[str] = mapped_column(String(32), index=True)
    type: Mapped[str] = mapped_column(String(8))
    weight: Mapped[int]
    coop_oid: Mapped[str] = mapped_column(
        ForeignKey("coops.oid", ondelete="CASCADE")
    )
    avg_eggs_per_month: Mapped[Optional[int]]

    coop: Mapped["Coop"] = relationship(
        uselist=False, back_populates="birds")

    @staticmethod
    def from_dto(bird_dto: BirdDTO) -> "Bird":
        bird = Bird(**asdict(bird_dto))
        return bird

    def to_dto(self) -> BirdDTO:
        bird_dict = deepcopy(self.__dict__)
        del bird_dict["_sa_instance_state"]
        del bird_dict["oid"]
        bird_dto = BirdDTO(**bird_dict)
        return bird_dto
