from http import HTTPStatus

from flask import Flask

from app.application.errorhandlers import handle_bad_request


def create_app():
    app = Flask(__name__)

    # Routing
    from app.application.views.birds import bp as bp__birds  # noqa
    app.register_blueprint(bp__birds)

    from app.application.views.coops import bp as bp__coops  # noqa
    app.register_blueprint(bp__coops)

    # Register handlers
    app.register_error_handler(HTTPStatus.BAD_REQUEST, handle_bad_request)

    return app


# Models
from app.infrastructure.models.coops import *  # noqa
from app.infrastructure.models.birds import *  # noqa
