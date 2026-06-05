"""
Request monitoring and health check utilities for Arvindu Hospitals
"""

import time
import uuid
import logging
from datetime import datetime
from flask import request, g, current_app, jsonify


class RequestMonitor:
    """Logs every request with timing info"""

    def init_app(self, app):
        app.before_request(self._before)
        app.after_request(self._after)
        app.teardown_appcontext(self._teardown)

    def _before(self):
        g.start_time = time.time()
        g.request_id = uuid.uuid4().hex[:8]
        current_app.logger.info(
            f"Request {g.request_id}: {request.method} {request.path} from {request.remote_addr}"
        )

    def _after(self, response):
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            current_app.logger.info(
                f"Response {g.request_id}: {response.status_code} in {duration:.3f}s"
            )
            if duration > 2.0:
                current_app.logger.warning(
                    f"Slow request {g.request_id}: {request.method} {request.path} "
                    f"took {duration:.3f}s"
                )
        return response

    def _teardown(self, exception):
        if exception:
            current_app.logger.error(
                f"Request {getattr(g, 'request_id', 'unknown')} failed: {exception}"
            )


def setup_logging(app):
    """Configure file logging for production"""
    if not app.debug and not app.testing:
        import os
        from logging.handlers import RotatingFileHandler
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


def init_monitoring(app):
    """Initialize monitoring: logging + request tracking + /health endpoint"""
    setup_logging(app)

    monitor = RequestMonitor()
    monitor.init_app(app)

    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
        })

    app.logger.info('Monitoring initialized successfully')
