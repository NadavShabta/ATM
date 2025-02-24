from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Flask-Migrate
from config.config import Config

db = SQLAlchemy()
migrate = Migrate()  # Initialize migration object


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to register them
    from app import models

    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

app = create_app()






