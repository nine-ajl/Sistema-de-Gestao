"""Application entry point for the inventory dashboard."""

import os
from typing import Tuple

from dotenv import load_dotenv
from flask import Flask, Response
from werkzeug.exceptions import InternalServerError, NotFound

load_dotenv()

from controllers.produto_controller import produto_bp
from models.produto_model import init_db
from utils.api_response import api_response


def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        The configured Flask application.
    """
    application = Flask(__name__)
    init_db()

    @application.errorhandler(404)
    def handle_not_found(_error: NotFound) -> Tuple[Response, int]:
        """Return the standard response for requests to unknown routes.

        Args:
            _error: The Flask 404 exception.

        Returns:
            A standard JSON error response and its HTTP status.
        """
        return api_response(
            success=False,
            data=None,
            message="A rota solicitada não foi encontrada.",
            status_code=_error.code or 404,
        )

    @application.errorhandler(500)
    def handle_internal_error(_error: InternalServerError) -> Tuple[Response, int]:
        """Return a safe standard response for unexpected server errors.

        Args:
            _error: The Flask 500 exception.

        Returns:
            A standard JSON error response and its HTTP status.
        """
        return api_response(
            success=False,
            data=None,
            message="Ocorreu um erro interno. Tente novamente mais tarde.",
            status_code=_error.code or 500,
        )

    application.register_blueprint(produto_bp)
    return application


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes", "on"}
    print("Servidor iniciado em: http://127.0.0.1:{}".format(port))
    app.run(host="127.0.0.1", port=port, debug=debug)
