"""
Performance optimizations for Arvindu Hospitals
"""

from flask import request, current_app
from werkzeug.middleware.proxy_fix import ProxyFix


def _add_static_cache_headers(response):
    """Cache static files for 1 year in production"""
    if request.endpoint == 'static' and not current_app.debug:
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response


def init_performance_optimizations(app):
    """Apply performance optimizations to the Flask app"""

    # Trust proxy headers in production (e.g., behind nginx/gunicorn)
    if not app.debug:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Long-lived cache for static assets
    app.after_request(_add_static_cache_headers)
