from dataclasses import dataclass

from app.exceptions import IncorrectValueError


@dataclass(frozen=True)
class FrontPaginationDTO:
    page: int
    items_per_page: int

    def __post_init__(self):
        self.__validate()

    def __validate(self):
        page = self.page
        if page <= 0:
            raise IncorrectValueError(f"Incorrect page: {page}")
        items_per_page = self.items_per_page
        if items_per_page <= 0:
            raise IncorrectValueError(
                f"Incorrect items_per_page: {items_per_page}")
