# network-device-manager-6400-6719

This workspace contains the Flask backend for a Network Device Manager.

- Backend: FlaskBackend/
  - Implements REST API for device CRUD and ping using Flask-RESTful, pymongo, and pythonping.
  - Configuration via environment variables in config.py (MONGO_URI, DB_NAME, COLLECTION_NAME) with sensible defaults:
    - MONGO_URI: mongodb://localhost:27017
    - DB_NAME: network_device_manager
    - COLLECTION_NAME: devices
  - If environment variables are not provided, the defaults above are used so the API runs out-of-the-box.
  - A .env.example file is provided with placeholders; copy to .env to customize.
  - CORS enabled for frontend compatibility.

See FlaskBackend/README.md for details.