# Network Device Manager - Flask Backend

This service provides a REST API for managing network devices and performing ping health checks.

Endpoints:
- GET /devices — list all devices
- POST /devices — create a device (unique name)
- GET /devices/{name} — get a device
- PUT /devices/{name} — update ip/type/location
- DELETE /devices/{name} — delete a device
- GET /ping/{name} — ping the device and return status and timestamp

Configuration (config.py via environment variables):
- MONGO_URI: MongoDB connection string (e.g., mongodb://localhost:27017)
- DB_NAME: Database name (default: network_device_manager)
- COLLECTION_NAME: Collection name (default: devices)

CORS is enabled for all origins for frontend integration.

Run:
- python run.py

Make sure your MongoDB instance is reachable based on MONGO_URI.
