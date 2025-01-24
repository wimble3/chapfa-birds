from dataclasses import dataclass


@dataclass(frozen=True)
class PaginationDTO:
    limit: int
    offset: int
