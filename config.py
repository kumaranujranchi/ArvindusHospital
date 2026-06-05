"""
Configuration management for Arvindu Hospitals website
"""

import os
from datetime import timedelta


class Config:
    """Base configuration"""

    SECRET_KEY = os.environ.get('SESSION_SECRET') or 'dev-secret-key-change-in-production'

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    SESSION_COOKIE_SECURE = False

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance', 'arvindu_hospitals.db')
    )

    @staticmethod
    def init_app(app):
        import logging
        logging.basicConfig(level=logging.DEBUG)
        os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
    }

    @staticmethod
    def init_app(app):
        import logging
        from logging.handlers import RotatingFileHandler

        if not app.debug and not app.testing:
            os.makedirs('logs', exist_ok=True)
            handler = RotatingFileHandler(
                'logs/arvindu_hospitals.log', maxBytes=10_240_000, backupCount=10
            )
            handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            handler.setLevel(logging.INFO)
            app.logger.addHandler(handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Arvindu Hospitals startup')

        required = ['DATABASE_URL', 'SESSION_SECRET']
        missing = [v for v in required if not os.environ.get(v)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


class TestingConfig(Config):
    """Testing configuration"""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False

    @staticmethod
    def init_app(app):
        import logging
        logging.disable(logging.CRITICAL)


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}


def get_config():
    """Return config class based on FLASK_ENV"""
    env = os.environ.get('FLASK_ENV', 'development').lower()
    return config.get(env, config['default'])
