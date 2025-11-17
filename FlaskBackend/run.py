from app import app

"""
Entrypoint script for running the Flask application.
Respects default port from environment (Flask default 5000).
"""

if __name__ == "__main__":
    app.run()
