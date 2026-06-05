import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from config import get_config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(config_name=None):
    """Application factory"""
    app = Flask(__name__)

    # Load configuration
    if config_name is None:
        config_class = get_config()
    else:
        from config import config
        config_class = config.get(config_name, config['default'])

    app.config.from_object(config_class)
    config_class.init_app(app)

    # Initialize extensions
    db.init_app(app)

    # Register routes
    from routes import register_routes
    register_routes(app)

    # Initialize monitoring and performance optimizations
    if not app.testing:
        from monitoring import init_monitoring
        from performance import init_performance_optimizations

        init_monitoring(app)
        init_performance_optimizations(app)

    return app


def init_database(app):
    """Initialize database tables"""
    with app.app_context():
        try:
            import models  # noqa: F401
            db.create_all()
            app.logger.info("Database tables initialized successfully")
        except Exception as e:
            app.logger.warning(f"Database initialization failed: {e}")
            app.logger.warning("Application will run without database functionality")


# Create the app instance
app = create_app()

# Initialize database for non-serverless environments
init_database(app)
