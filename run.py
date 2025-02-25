"""
Entry point for the ATM System Flask application.
Automatically initializes the database and starts the server.
"""

from app import app

if __name__ == '__main__':
    # Start the Flask development server
    app.run(host="127.0.0.1", port=5000)

