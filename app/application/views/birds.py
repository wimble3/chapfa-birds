from http import HTTPStatus

from flask import (
    Blueprint, render_template, request, redirect, url_for, abort)
from punq import Container
from sqlalchemy.orm import Session

from app import handle_bad_request
from app.application.dtos.front_pagination_dto import FrontPaginationDTO
from app.application.errorhandlers import handle_internal_server_error
from app.application.use_cases.birds import (
    CreateBirdUseCase, GetBirdsByCoopUseCase, UpdateBirdUseCase,
    DeleteBirdUseCase)
from app.application.use_cases.coops import GetCoopStatisticUseCase
from app.container import get_container
from app.domain.entities.birds import BirdTypeEnum, BirdDTO, UpdateBirdDTO
from app.exceptions import UserError, ApplicationError
from app.infrastructure.repositories.birds import BaseBirdRepository
from app.infrastructure.repositories.coops import BaseCoopRepository
from settings import Settings


BP_NAME = "birds"
bp = Blueprint(
    name=BP_NAME,
    import_name=__name__,
    url_prefix="",
    template_folder=Settings.TEMPLATE_PREFIX
)


@bp.route(
    "/coops/<uuid:coop_oid>/birds", defaults={"page": 1}, methods=["GET"])
@bp.route("/coops/<uuid:coop_oid>/birds/<int:page>", methods=["GET"])
def listing(
        coop_oid: str,
        page: int = 1,
        container: Container = get_container()
):
    try:
        with container.resolve(Session) as db:
            front_pagination_dto = FrontPaginationDTO(
                page=page, items_per_page=Settings.BIRDS_ITEMS_PER_PAGE)

            get_birds_use_case = GetBirdsByCoopUseCase(
                bird_repo=container.resolve(BaseBirdRepository)(db=db)
            )
            birds, total_pages = get_birds_use_case.execute(
                coop_oid, front_pagination_dto)

            get_coop_stat_use_case = GetCoopStatisticUseCase(
                coop_repo=container.resolve(BaseCoopRepository)(db=db)
            )
            coop_statistic = get_coop_stat_use_case.execute(coop_oid)

            context = {
                "coop_oid": coop_oid,
                "birds": birds,
                "page": page,
                "total_pages": total_pages,
                "items_per_page": front_pagination_dto.items_per_page,
                "len_birds": len(birds),
                "coop_statistic": coop_statistic
            }
            return render_template(
                template_name_or_list=f"{BP_NAME}/list.html", **context)
    except UserError as e:
        return handle_bad_request(e)
    except ApplicationError as e:
        return handle_internal_server_error(e)


@bp.route("/coops/<uuid:coop_oid>/birds/create", methods=["GET", "POST"])
def create(coop_oid: str, container: Container = get_container()):
    try:
        with container.resolve(Session) as db:
            bird_types = [bird_type.value for bird_type in BirdTypeEnum]

            if request.method == "POST":
                name = request.form["name"]
                type_ = request.form["type"]
                weight = int(request.form["weight"])
                avg_eggs_per_month = request.form["avg_eggs_per_month"]

                bird_dto = BirdDTO(
                    name=name, type=type_,
                    weight=weight,
                    avg_eggs_per_month=avg_eggs_per_month or None,
                    coop_oid=coop_oid
                )

                use_case = CreateBirdUseCase(
                    bird_repo=container.resolve(BaseBirdRepository)(db=db)
                )
                use_case.execute(bird_dto)

                context = {
                    "coop_oid": coop_oid
                }
                endpoint = url_for("birds.listing", **context)
                return redirect(endpoint)

            context = {
                "coop_oid": coop_oid,
                "bird_types": bird_types
            }
            return render_template(
                template_name_or_list=f"{BP_NAME}/create.html", **context)
    except UserError as e:
        return handle_bad_request(e)
    except ApplicationError as e:
        return handle_internal_server_error(e)


@bp.route("/birds/delete/<uuid:bird_oid>", methods=["DELETE"])
def delete(bird_oid: str, container: Container = get_container()):
    try:
        with container.resolve(Session) as db:
            use_case = DeleteBirdUseCase(
                bird_repo=container.resolve(BaseBirdRepository)(db=db)
            )
            use_case.execute(bird_oid)
            return {"result": True}
    except UserError as e:
        return handle_bad_request(e)
    except ApplicationError as e:
        return handle_internal_server_error(e)


@bp.route("/birds/update/<uuid:bird_oid>", methods=["PATCH"])
def update(bird_oid: str, container: Container = get_container()):
    try:
        with container.resolve(Session) as db:
            update_bird_dict = {
                request.json["field"]: request.json["value"]
            }
            update_bird_dto = UpdateBirdDTO(**update_bird_dict)
            use_case = UpdateBirdUseCase(
                bird_repo=container.resolve(BaseBirdRepository)(db=db)
            )
            use_case.execute(bird_oid, update_bird_dto)
            return {"status": True}
    except UserError as e:
        return handle_bad_request(e)
    except ApplicationError as e:
        return handle_internal_server_error(e)
