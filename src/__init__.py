from flask import Flask, jsonify
from .routes import views_blueprint, api_blueprint
from .services import vosk_service
from src.errors.errors import APIError


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)

    # Register Blueprints
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(views_blueprint)

    # Load Vosk model
    vosk_service.init_model()

    @app.errorhandler(APIError)
    def handle_api_error(e: APIError):
        payload = e.to_dict()
        return jsonify(payload), e.status_code

    return app
