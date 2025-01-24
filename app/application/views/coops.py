from flask import Blueprint, render_template, request, redirect, url_for
from punq import Container
from sqlalchemy.orm import Session

from app.application.errorhandlers import handle_bad_request, \
    handle_internal_server_error
from app.application.use_cases.coops import (
    GetCoopsUseCase, CreateCoopUseCase, DeleteCoopUseCase, UpdateCoopUseCase)
from app.container import get_container
from app.domain.entities.coops import CoopDTO, UpdateCoopDTO
from app.exceptions import UserError, ApplicationError
from app.infrastructure.repositories.coops import BaseCoopRepository
from settings import Settings


BP_NAME = "coops"
bp = Blueprint(
    name=BP_NAME,
    import_name=__name__,
    url_prefix="",
    template_folder=Settings.TEMPLATE_PREFIX
)


@bp.route("/", methods=["GET"])
def index(container: Container = get_container()):
    try:
        with container.resolve(Session) as db:
            use_case = GetCoopsUseCase(
                coop_repo=container.resolve(BaseCoopRepository)(db=db)
            )
            coops = use_case.execute()
            context = {
                "coops": coops
            }
            return render_template(
                template_name_or_list=f"{BP_NAME}/list.html", **context)
    except UserError as e:
        return handle_bad_request(e)
    except ApplicationError as e:
        return handle_internal_server_error(e)


@bp.route("/create", methods=["GET", "POST"])
def create(container: Container = get_container()):
    try:
        with container.resolve(Session) as db:
            if request.method == "POST":
                name = request.form["name"]
                capacity = int(request.form["capacity"])

                coop_dto = CoopDTO(name=name, capacity=capacity)
                use_case = CreateCoopUseCase(
                    coop_repo=container.resolve(BaseCoopRepository)(db=db)
                )
                use_case.execute(coop_dto)
                return redirect(location="/")

            return render_template(
                template_name_or_list=f"{BP_NAME}/create.html")
    except UserError as e:
        return handle_bad_request(e)
    except ApplicationError as e:
        return handle_internal_server_error(e)


@bp.route("/delete/<uuid:coop_oid>", methods=["DELETE"])
def delete(coop_oid: str, container: Container = get_container()):
    try:
        with container.resolve(Session) as db:
            use_case = DeleteCoopUseCase(
                coop_repo=container.resolve(BaseCoopRepository)(db=db)
            )
            use_case.execute(coop_oid)
            return url_for("coops.index", _method="GET")
    except UserError as e:
        return handle_bad_request(e)
    except ApplicationError as e:
        return handle_internal_server_error(e)


@bp.route("/update/<uuid:coop_oid>", methods=["PATCH"])
def update(coop_oid: str, container: Container = get_container()):
    try:
        with container.resolve(Session) as db:
            update_coop_dict = {
                request.json["field"]: request.json["value"]
            }
            update_coop_dto = UpdateCoopDTO(**update_coop_dict)
            use_case = UpdateCoopUseCase(
                coop_repo=container.resolve(BaseCoopRepository)(db=db)
            )
            use_case.execute(coop_oid, update_coop_dto)
            return {"result": True}
    except UserError as e:
        return handle_bad_request(e)
    except ApplicationError as e:
        return handle_internal_server_error(e)
