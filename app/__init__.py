# /app/__init__.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
import logging
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # Настройка логирования
    logging.basicConfig(level=app.config['LOGGING_LEVEL'],
                        format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.FileHandler("app.log"),
                                  logging.StreamHandler()])

    from app.routes import calls_bp, call_records_bp, phones_bp
    app.register_blueprint(calls_bp)
    app.register_blueprint(call_records_bp)
    app.register_blueprint(phones_bp)

    # Обработка ошибок
    @app.errorhandler(404)
    def not_found_error(error):
        logging.error("404 error: %s", error)
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logging.error("500 error: %s", error)
        return jsonify({'error': 'Internal server error'}), 500

    # Swagger UI
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "MegaFon API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
