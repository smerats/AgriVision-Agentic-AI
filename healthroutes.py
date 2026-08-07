"""
routes/health_routes.py
Simple liveness/health-check endpoint for the AgriVision AI backend.
"""

from flask import Blueprint
from controllers.prediction_controller import health_check

health_bp = Blueprint("health_bp", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    return health_check()