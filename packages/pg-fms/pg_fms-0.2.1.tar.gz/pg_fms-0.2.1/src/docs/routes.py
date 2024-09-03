from flask import Flask, render_template
import sentry_sdk

sentry_sdk.init(
    dsn="https://8e15628cf1f77291993ad38cfd191bfc@o4506762839916544.ingest.us.sentry.io/4507884247908352",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def landing_page():
    """Landing page for the application."""
    return render_template("home.jinja2"), 200


@app.errorhandler(404)
def catch_all(subpath: str):
    """Catch all route for the application."""
    sentry_sdk.capture_message(f"404: Page not found for {subpath}")
    return render_template("dom/404.jinja2"), 404


@app.errorhandler(500)
def handle_internal_server_error(e: Exception):
    """Handle internal server errors."""
    sentry_sdk.capture_exception(e)
    return render_template("dom/500.jinja2"), 500

if __name__ == "__main__":
    app.run(debug=False)
