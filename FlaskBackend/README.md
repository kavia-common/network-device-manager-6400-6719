# Network Device Manager - Flask Backend

This service provides a REST API for managing network devices and performing ping health checks.

Endpoints:
- GET /devices — list all devices
- POST /devices — create a device (unique name)
- GET /devices/{name} — get a device
- PUT /devices/{name} — update ip/type/location
- DELETE /devices/{name} — delete a device
- GET /ping/{name} — ping the device and return status and timestamp

Configuration (config.py via environment variables with defaults):
- MONGO_URI: MongoDB connection string. Default if not set: mongodb://localhost:27017
- DB_NAME: Database name. Default if not set: network_device_manager
- COLLECTION_NAME: Collection name. Default if not set: devices

Notes:
- The application will use the defaults above when corresponding environment variables are not provided. This enables running the API out-of-the-box without a .env file.
- You can still create a .env file to override these values. See .env.example for placeholders; if any value is omitted, the default listed above will be used.

CORS is enabled for all origins for frontend integration.

Run:
- python run.py

Make sure your MongoDB instance is reachable based on MONGO_URI (or the default localhost URI).
