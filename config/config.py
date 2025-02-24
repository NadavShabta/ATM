import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class that holds default settings for the application.
    """

    # Enable/disable debug mode.
    DEBUG = False

    # Secret key for security-related tasks.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

    # Correct database path for SQLite
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'instance', 'atm.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """
    Development configuration class.
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configuration class.
    """
    DEBUG = False
