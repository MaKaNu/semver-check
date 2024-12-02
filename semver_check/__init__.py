import flask
from flask import Flask, jsonify, render_template, request

from semver_check.server import is_valid_semver

app = Flask(__name__)


@app.route("/")
def home() -> str:
    """Serve the main HTML page."""
    return render_template("index.html")


@app.route("/validate", methods=["POST"])
def validate_version() -> tuple[flask.wrappers.Response | str, int]:
    """Endpoint to validate SemVer strings."""
    request.get_data(as_text=True)
    version = request.data.decode("utf-8").strip()  # Get raw text from the body
    if not version:
        return "Version string missing in the request body", 400

    if is_valid_semver(version):
        # Respond with HTTP 200 for valid versions
        return jsonify({"version": version, "valid": True}), 200
    else:
        # Respond with HTTP 400 for invalid versions
        return jsonify({"version": version, "valid": False}), 400
