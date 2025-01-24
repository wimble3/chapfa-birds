from app.application.dtos.front_pagination_dto import FrontPaginationDTO
from app.infrastructure.dtos.pagination_dto import PaginationDTO


class DTOHelper:
    @staticmethod
    def pagination_dto_from_front(
            front_pagination_dto: FrontPaginationDTO
    ) -> PaginationDTO:
        limit = front_pagination_dto.items_per_page
        offset = (front_pagination_dto.page - 1) * limit
        pagination_dto = PaginationDTO(limit=limit, offset=offset)
        return pagination_dto
