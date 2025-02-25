"""
Flask Application Factory

This module is responsible for setting up and configuring the Flask application.
It initializes the database, registers models, and sets up routes.
Additionally, it ensures the database is properly initialized before the app starts.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    This function:
    - Initializes the Flask app with configuration settings.
    - Registers the database and models.
    - Registers application blueprints.
    - Ensures the database is set up before the app starts.

    Args:
        config_class (Config): The configuration class to use.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database with the Flask app
    db.init_app(app)

    # Import models to register them
    from app import models

    # Register Blueprints
    from app.routes.account_routes import bp as account_bp
    app.register_blueprint(account_bp)

    # Initialize the database automatically when the app starts
    with app.app_context():
        from db_setup import initialize_database
        initialize_database()

    return app

# Create the application instance
app = create_app()
