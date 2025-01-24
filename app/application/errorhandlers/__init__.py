from http import HTTPStatus

from flask import render_template

from app.exceptions import UserError, ApplicationError


def handle_bad_request(e: UserError) -> tuple[str, int]:
    return (
        render_template("error.html", context={"e": e}),
        HTTPStatus.BAD_REQUEST
    )


def handle_internal_server_error(e: ApplicationError) -> tuple[str, int]:
    return (
        render_template("app_error.html", context={"e": e}),
        HTTPStatus.INTERNAL_SERVER_ERROR
    )
