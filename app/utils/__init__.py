# /app/utils/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Настройка логирования
    logging.basicConfig(level=app.config['LOGGING_LEVEL'],
                        format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.FileHandler("app.log"),
                                  logging.StreamHandler()])

    from app.routes import calls, call_records, phones
    app.register_blueprint(calls.bp)
    app.register_blueprint(call_records.bp)
    app.register_blueprint(phones.bp)

    return app
