from flask import Flask
from . import routes
import logging


def create_app():
    """Construct the core application."""
    app = Flask(__name__, template_folder="templates")
    app.static_folder = "static"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    with app.app_context():
        app.add_url_rule("/", view_func=routes.landing_page)
        app.add_url_rule("/<path:subpath>", view_func=routes.catch_all)

        return app
