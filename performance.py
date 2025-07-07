#!/usr/bin/env python3
"""
Performance optimization utilities for Arvindu Hospitals website
Includes caching, compression, and other performance enhancements
"""

import os
import gzip
import functools
from datetime import datetime, timedelta
from flask import request, make_response, current_app, g
from werkzeug.middleware.proxy_fix import ProxyFix

class CacheManager:
    """Simple in-memory cache for frequently accessed data"""
    
    def __init__(self):
        self._cache = {}
        self._timestamps = {}
        self.default_timeout = 300  # 5 minutes
    
    def get(self, key):
        """Get value from cache"""
        if key in self._cache:
            # Check if cache entry is still valid
            if key in self._timestamps:
                age = datetime.utcnow() - self._timestamps[key]
                if age.total_seconds() < self.default_timeout:
                    return self._cache[key]
                else:
                    # Cache expired, remove it
                    self.delete(key)
        return None
    
    def set(self, key, value, timeout=None):
        """Set value in cache"""
        self._cache[key] = value
        self._timestamps[key] = datetime.utcnow()
        
        # Clean up old entries periodically
        if len(self._cache) > 100:  # Arbitrary limit
            self._cleanup()
    
    def delete(self, key):
        """Delete value from cache"""
        self._cache.pop(key, None)
        self._timestamps.pop(key, None)
    
    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()
        self._timestamps.clear()
    
    def _cleanup(self):
        """Remove expired cache entries"""
        now = datetime.utcnow()
        expired_keys = []
        
        for key, timestamp in self._timestamps.items():
            age = now - timestamp
            if age.total_seconds() >= self.default_timeout:
                expired_keys.append(key)
        
        for key in expired_keys:
            self.delete(key)

# Global cache instance
cache = CacheManager()

def cached(timeout=300, key_func=None):
    """Decorator for caching function results"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        
        return wrapper
    return decorator

class CompressionMiddleware:
    """Middleware for compressing responses"""
    
    def __init__(self, app, compress_level=6):
        self.app = app
        self.compress_level = compress_level
    
    def __call__(self, environ, start_response):
        """WSGI middleware for compression"""
        def new_start_response(status, response_headers):
            # Check if client accepts gzip
            accept_encoding = environ.get('HTTP_ACCEPT_ENCODING', '')
            if 'gzip' not in accept_encoding:
                return start_response(status, response_headers)
            
            # Check content type
            content_type = None
            for header in response_headers:
                if header[0].lower() == 'content-type':
                    content_type = header[1]
                    break
            
            # Only compress text-based content
            if content_type and any(ct in content_type.lower() for ct in 
                                  ['text/', 'application/json', 'application/javascript', 'application/xml']):
                response_headers.append(('Content-Encoding', 'gzip'))
                response_headers.append(('Vary', 'Accept-Encoding'))
            
            return start_response(status, response_headers)
        
        return self.app(environ, new_start_response)

def add_cache_headers(response, max_age=3600):
    """Add cache headers to response"""
    if not current_app.debug:
        response.headers['Cache-Control'] = f'public, max-age={max_age}'
        response.headers['Expires'] = (
            datetime.utcnow() + timedelta(seconds=max_age)
        ).strftime('%a, %d %b %Y %H:%M:%S GMT')
    return response

def optimize_static_files(app):
    """Optimize static file serving"""
    @app.after_request
    def add_static_cache_headers(response):
        """Add cache headers for static files"""
        if request.endpoint == 'static':
            # Cache static files for 1 year
            return add_cache_headers(response, max_age=31536000)
        return response

def optimize_database_queries(app):
    """Optimize database query performance"""
    from app import db

    with app.app_context():
        # Enable query logging in debug mode
        if app.debug:
            import logging
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

        # Set up connection pooling optimization
        if hasattr(db.engine, 'pool'):
            db.engine.pool._recycle = 3600  # Recycle connections every hour

class PerformanceProfiler:
    """Simple performance profiler for development"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize profiler with Flask app"""
        if app.debug:
            app.before_request(self.before_request)
            app.after_request(self.after_request)
    
    def before_request(self):
        """Start timing request"""
        import time
        g.start_time = time.time()
    
    def after_request(self, response):
        """Log request timing"""
        if hasattr(g, 'start_time'):
            import time
            duration = time.time() - g.start_time
            duration_ms = duration * 1000

            current_app.logger.debug(
                f"Request {request.method} {request.path} "
                f"completed in {duration_ms:.2f}ms"
            )

        return response

def init_performance_optimizations(app):
    """Initialize all performance optimizations"""
    
    # Add proxy fix for production deployments
    if not app.debug:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Optimize static file serving
    optimize_static_files(app)
    
    # Optimize database queries
    optimize_database_queries(app)
    
    # Initialize profiler for development
    if app.debug:
        profiler = PerformanceProfiler(app)
    
    # Add performance-related routes
    @app.route('/performance/cache/clear')
    def clear_cache():
        """Clear application cache (development only)"""
        if not app.debug:
            from flask import abort
            abort(404)
        
        cache.clear()
        return {'status': 'cache cleared'}
    
    @app.route('/performance/stats')
    def performance_stats():
        """Get performance statistics (development only)"""
        if not app.debug:
            from flask import abort
            abort(404)
        
        from flask import jsonify
        stats = {
            'cache_size': len(cache._cache),
            'cache_keys': list(cache._cache.keys()),
            'timestamp': datetime.utcnow().isoformat()
        }
        return jsonify(stats)

# Cached functions for common queries
@cached(timeout=600)  # Cache for 10 minutes
def get_department_list():
    """Get list of departments (cached)"""
    # This would typically come from database
    return [
        'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics',
        'Gynecology', 'Dermatology', 'Ophthalmology', 'ENT',
        'Gastroenterology', 'Oncology'
    ]

@cached(timeout=3600)  # Cache for 1 hour
def get_doctor_list():
    """Get list of doctors (cached)"""
    # This would typically come from database
    return [
        {'name': 'Dr. Sharma', 'department': 'Cardiology'},
        {'name': 'Dr. Patel', 'department': 'Neurology'},
        {'name': 'Dr. Singh', 'department': 'Orthopedics'},
        {'name': 'Dr. Gupta', 'department': 'Pediatrics'},
        {'name': 'Dr. Kumar', 'department': 'Gynecology'},
    ]

def minify_html(html):
    """Simple HTML minification"""
    if current_app.debug:
        return html
    
    import re
    # Remove extra whitespace
    html = re.sub(r'\s+', ' ', html)
    # Remove whitespace around tags
    html = re.sub(r'>\s+<', '><', html)
    return html.strip()

class HTMLMinifyMiddleware:
    """Middleware to minify HTML responses"""
    
    def __init__(self, app):
        self.app = app
        app.after_request(self.minify_response)
    
    def minify_response(self, response):
        """Minify HTML responses"""
        if (response.content_type and 
            'text/html' in response.content_type and 
            not current_app.debug):
            
            response.data = minify_html(response.get_data(as_text=True)).encode('utf-8')
        
        return response
