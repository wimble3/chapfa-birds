from app.infrastructure.database.base import session


from punq import Container

from sqlalchemy.orm import Session

from app.infrastructure.repositories.birds import BaseBirdRepository, \
    BirdRepository
from app.infrastructure.repositories.coops import (
    BaseCoopRepository, CoopRepository)


def get_db() -> Session:
    return session()


def get_container():
    container = Container()

    # Database session
    container.register(Session, factory=get_db)

    # Repositories
    container.register(BaseCoopRepository, lambda: CoopRepository)
    container.register(BaseBirdRepository, lambda: BirdRepository)

    return container
