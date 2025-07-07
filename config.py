#!/usr/bin/env python3
"""
Configuration management for Arvindu Hospitals website
Handles different environments (development, production, testing)
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SESSION_SECRET') or 'dev-secret-key-change-in-production'
    
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # WTF settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # Application settings
    HOSPITAL_NAME = "Arvindu Hospitals"
    HOSPITAL_TAGLINE = "Care with Compassion"
    
    # Email settings (for future use)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Pagination
    APPOINTMENTS_PER_PAGE = 20
    MESSAGES_PER_PAGE = 20
    
    @staticmethod
    def init_app(app):
        """Initialize application with this config"""
        pass

class DevelopmentConfig(Config):
    """Development environment configuration"""
    
    DEBUG = True
    TESTING = False
    
    # Use SQLite for local development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance', 'arvindu_hospitals.db')
    
    # Less strict security for development
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = True
    
    @staticmethod
    def init_app(app):
        """Initialize development app"""
        import logging
        logging.basicConfig(level=logging.DEBUG)
        
        # Create instance directory if it doesn't exist
        instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
        os.makedirs(instance_dir, exist_ok=True)

class ProductionConfig(Config):
    """Production environment configuration"""
    
    DEBUG = False
    TESTING = False
    
    # Production database (required)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Strict security settings
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True
    
    # Performance settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
    }
    
    @staticmethod
    def init_app(app):
        """Initialize production app"""
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Set up file logging
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = RotatingFileHandler(
                'logs/arvindu_hospitals.log',
                maxBytes=10240000,  # 10MB
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('Arvindu Hospitals startup')
        
        # Validate required environment variables
        required_vars = ['DATABASE_URL', 'SESSION_SECRET']
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

class TestingConfig(Config):
    """Testing environment configuration"""
    
    DEBUG = True
    TESTING = True
    
    # Use in-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    
    @staticmethod
    def init_app(app):
        """Initialize testing app"""
        import logging
        logging.disable(logging.CRITICAL)

class NetlifyConfig(ProductionConfig):
    """Netlify-specific production configuration"""

    # Use SQLite as fallback if no database URL is provided
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///temp_arvindu_hospitals.db'

    @staticmethod
    def init_app(app):
        """Initialize Netlify app"""
        # Don't call ProductionConfig.init_app to avoid required env var validation
        import logging

        # Set up basic logging
        app.logger.setLevel(logging.INFO)
        app.logger.info('Running on Netlify Functions')

        # Handle database URL for different providers
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            if database_url.startswith('postgres://'):
                # Fix for newer SQLAlchemy versions
                os.environ['DATABASE_URL'] = database_url.replace('postgres://', 'postgresql://', 1)
                app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
            app.logger.info('Using external database')
        else:
            app.logger.info('Using SQLite fallback database')

        # Validate only critical environment variables
        session_secret = os.environ.get('SESSION_SECRET')
        if not session_secret:
            app.logger.warning('SESSION_SECRET not set, using default (not secure)')
            app.config['SECRET_KEY'] = 'netlify-default-key-change-in-production'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'netlify': NetlifyConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development').lower()
    
    # Auto-detect Netlify environment
    if os.environ.get('NETLIFY'):
        env = 'netlify'
    
    return config.get(env, config['default'])
