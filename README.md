# network-device-manager-6400-6719

This workspace contains the Flask backend for a Network Device Manager.

- Backend: FlaskBackend/
  - Implements REST API for device CRUD and ping using Flask-RESTful, pymongo, and pythonping.
  - Configuration via environment variables in config.py (MONGO_URI, DB_NAME, COLLECTION_NAME).
  - CORS enabled for frontend compatibility.

See FlaskBackend/README.md for details.