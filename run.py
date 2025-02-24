# run.py

"""
Entry point for the ATM System Flask application.
This script imports the configured Flask app from the app package and starts the server.
For production deployments, consider using a production-grade WSGI server such as Gunicorn.
"""

from app import app

if __name__ == '__main__':
    # Run the Flask development server on the default port (5000).
    # The debug mode is enabled here for development purposes.
    app.run(debug=True)
