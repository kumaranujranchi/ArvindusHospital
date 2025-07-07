import os
import sys
import json
from urllib.parse import unquote

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Set environment to production for Netlify
os.environ.setdefault('FLASK_ENV', 'netlify')

def handler(event, context):
    """
    Netlify Functions handler for Flask app
    """
    try:
        # Import app here to avoid issues with initialization
        from app import create_app, init_database

        # Create app instance for this request
        app = create_app('netlify')

        # Initialize database if available
        try:
            init_database(app)
        except Exception as db_error:
            app.logger.warning(f"Database initialization failed: {db_error}")

        # Get the HTTP method and path
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')

        # Remove the /.netlify/functions/app prefix if present
        if path.startswith('/.netlify/functions/app'):
            path = path[len('/.netlify/functions/app'):]

        if not path:
            path = '/'

        # Get query parameters
        query_string = event.get('queryStringParameters') or {}

        # Get headers
        headers = event.get('headers', {})

        # Get body
        body = event.get('body', '')
        if event.get('isBase64Encoded', False):
            import base64
            body = base64.b64decode(body).decode('utf-8')

        # Create a test client and make the request
        with app.test_client() as client:
            response = client.open(
                path=path,
                method=http_method,
                headers=headers,
                data=body,
                query_string=query_string
            )

            # Convert headers to dict
            response_headers = {}
            for key, value in response.headers:
                response_headers[key] = value

            # Return the response
            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response.get_data(as_text=True),
                'isBase64Encoded': False
            }

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in handler: {error_details}")

        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/html'},
            'body': f'''
            <h1>Arvindu Hospitals - Temporary Error</h1>
            <p>The application is starting up. Please refresh the page in a moment.</p>
            <p>Error: {str(e)}</p>
            <details>
                <summary>Technical Details</summary>
                <pre>{error_details}</pre>
            </details>
            ''',
            'isBase64Encoded': False
        }
