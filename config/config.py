"""
Configuration Settings for the ATM System

This module defines the configuration settings for different environments, including:
- Development settings
- Production settings
- Database configuration
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class that holds default settings for the application.

    Attributes:
        DEBUG (bool): Whether debug mode is enabled.
        SECRET_KEY (str): Secret key for session management and security.
        SQLALCHEMY_DATABASE_URI (str): Database connection URI.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Controls SQLAlchemy event system.
    """

    DEBUG = False  # Disable debug mode by default
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')  # Default secret key
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Use an in-memory SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to improve performance


class DevelopmentConfig(Config):
    """
    Development configuration class.

    Inherits from Config and enables debug mode for development environments.
    """

    DEBUG = True


class ProductionConfig(Config):
    """
    Production configuration class.

    Inherits from Config and ensures debug mode is disabled for production environments.
    """

    DEBUG = False
