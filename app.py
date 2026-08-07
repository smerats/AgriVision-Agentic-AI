"""
app.py
Entry point for the AgriVision AI backend.
Wires together routes/controllers/services using a simple Flask
application factory. Only the AI Prediction Engine + Backend module
lives here -- no frontend, satellite, recommendation, or database code.
"""

from flask import Flask

from config import Config
from routes.prediction_routes import prediction_bp
from routes.health_routes import health_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register route blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(prediction_bp, url_prefix="/predict")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)