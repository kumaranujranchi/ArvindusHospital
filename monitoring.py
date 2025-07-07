#!/usr/bin/env python3
"""
Monitoring and logging utilities for Arvindu Hospitals website
Provides application monitoring, error tracking, and performance metrics
"""

import os
import time
import logging
import functools
from datetime import datetime, timedelta
from flask import request, g, current_app
from app import db

class ApplicationMonitor:
    """Application monitoring and metrics collection"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize monitoring with Flask app"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_appcontext(self.teardown_request)
        
        # Set up error handlers
        app.errorhandler(404)(self.handle_404)
        app.errorhandler(500)(self.handle_500)
        app.errorhandler(Exception)(self.handle_exception)
    
    def before_request(self):
        """Called before each request"""
        g.start_time = time.time()
        g.request_id = self.generate_request_id()
        
        # Log request details
        current_app.logger.info(
            f"Request {g.request_id}: {request.method} {request.path} "
            f"from {request.remote_addr}"
        )
    
    def after_request(self, response):
        """Called after each request"""
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            
            # Log response details
            current_app.logger.info(
                f"Response {g.request_id}: {response.status_code} "
                f"in {duration:.3f}s"
            )
            
            # Log slow requests
            if duration > 2.0:  # Requests taking more than 2 seconds
                current_app.logger.warning(
                    f"Slow request {g.request_id}: {request.method} {request.path} "
                    f"took {duration:.3f}s"
                )
        
        return response
    
    def teardown_request(self, exception):
        """Called when request context is torn down"""
        if exception:
            current_app.logger.error(
                f"Request {getattr(g, 'request_id', 'unknown')} failed: {exception}"
            )
    
    def handle_404(self, error):
        """Handle 404 errors"""
        current_app.logger.warning(
            f"404 Error: {request.method} {request.path} from {request.remote_addr}"
        )
        from flask import render_template
        from forms import NewsletterForm
        newsletter_form = NewsletterForm()
        return render_template('404.html', newsletter_form=newsletter_form), 404
    
    def handle_500(self, error):
        """Handle 500 errors"""
        current_app.logger.error(
            f"500 Error: {request.method} {request.path} from {request.remote_addr}: {error}"
        )
        from flask import render_template
        from forms import NewsletterForm
        newsletter_form = NewsletterForm()
        return render_template('500.html', newsletter_form=newsletter_form), 500
    
    def handle_exception(self, error):
        """Handle uncaught exceptions"""
        current_app.logger.error(
            f"Unhandled exception: {request.method} {request.path} "
            f"from {request.remote_addr}: {error}",
            exc_info=True
        )
        return self.handle_500(error)
    
    @staticmethod
    def generate_request_id():
        """Generate a unique request ID"""
        import uuid
        return str(uuid.uuid4())[:8]

class DatabaseMonitor:
    """Database monitoring and health checks"""
    
    @staticmethod
    def check_database_health():
        """Check database connectivity and basic health"""
        try:
            # Simple connectivity test
            db.session.execute(db.text('SELECT 1'))
            
            # Check table existence
            from models import Appointment, ContactMessage, Newsletter
            tables = [Appointment, ContactMessage, Newsletter]
            
            for table in tables:
                count = db.session.query(table).count()
                current_app.logger.debug(f"Table {table.__tablename__}: {count} records")
            
            return True
        except Exception as e:
            current_app.logger.error(f"Database health check failed: {e}")
            return False
    
    @staticmethod
    def get_database_stats():
        """Get database statistics"""
        try:
            from models import Appointment, ContactMessage, Newsletter
            
            stats = {
                'appointments': db.session.query(Appointment).count(),
                'contact_messages': db.session.query(ContactMessage).count(),
                'newsletter_subscribers': db.session.query(Newsletter).count(),
                'recent_appointments': db.session.query(Appointment).filter(
                    Appointment.created_at >= datetime.utcnow() - timedelta(days=7)
                ).count(),
                'recent_messages': db.session.query(ContactMessage).filter(
                    ContactMessage.created_at >= datetime.utcnow() - timedelta(days=7)
                ).count(),
            }
            
            return stats
        except Exception as e:
            current_app.logger.error(f"Failed to get database stats: {e}")
            return {}

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            if duration > 1.0:  # Log functions taking more than 1 second
                current_app.logger.warning(
                    f"Slow function {func.__name__} took {duration:.3f}s"
                )
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            current_app.logger.error(
                f"Function {func.__name__} failed after {duration:.3f}s: {e}"
            )
            raise
    
    return wrapper

class HealthCheck:
    """Application health check endpoints"""
    
    @staticmethod
    def basic_health():
        """Basic health check"""
        return {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }
    
    @staticmethod
    def detailed_health():
        """Detailed health check including database"""
        health = HealthCheck.basic_health()
        
        # Database health
        db_healthy = DatabaseMonitor.check_database_health()
        health['database'] = 'healthy' if db_healthy else 'unhealthy'
        
        # Database stats
        if db_healthy:
            health['database_stats'] = DatabaseMonitor.get_database_stats()
        
        # Overall status
        health['status'] = 'healthy' if db_healthy else 'degraded'
        
        return health

def setup_logging(app):
    """Set up application logging"""
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Set up file handler
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            'logs/arvindu_hospitals.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        # Set up formatter
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Add handler to app logger
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Arvindu Hospitals application startup')

def init_monitoring(app):
    """Initialize all monitoring components"""
    # Set up logging
    setup_logging(app)
    
    # Initialize application monitor
    monitor = ApplicationMonitor(app)
    
    # Add health check routes
    @app.route('/health')
    def health_check():
        """Basic health check endpoint"""
        from flask import jsonify
        return jsonify(HealthCheck.basic_health())
    
    @app.route('/health/detailed')
    def detailed_health_check():
        """Detailed health check endpoint"""
        from flask import jsonify
        health = HealthCheck.detailed_health()
        status_code = 200 if health['status'] == 'healthy' else 503
        return jsonify(health), status_code
    
    app.logger.info('Monitoring initialized successfully')
