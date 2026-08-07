"""
routes/prediction_routes.py
Defines the /predict/* API surface. Each route simply delegates to the
matching controller function -- no business logic lives here.
"""

from flask import Blueprint
from controllers.prediction_controller import (
    predict_crop_yield,
    predict_disease,
    predict_pest,
    predict_climate,
)

prediction_bp = Blueprint("prediction_bp", __name__)


@prediction_bp.route("/crop-yield", methods=["POST"])
def crop_yield_route():
    return predict_crop_yield()


@prediction_bp.route("/disease", methods=["POST"])
def disease_route():
    return predict_disease()


@prediction_bp.route("/pest", methods=["POST"])
def pest_route():
    return predict_pest()


@prediction_bp.route("/climate", methods=["POST"])
def climate_route():
    return predict_climate()
