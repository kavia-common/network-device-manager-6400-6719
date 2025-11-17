from flask import request
from flask_restful import Resource
from pymongo.errors import DuplicateKeyError, PyMongoError
from pythonping import ping

from .db import get_devices_collection
from .utils import (
    validate_device_create,
    validate_device_update,
    serialize_device,
    error_response,
    current_timestamp_iso,
)


class DevicesResource(Resource):
    """
    Devices collection resource.
    - GET /devices: list all devices
    - POST /devices: create new device (unique name)
    """

    # PUBLIC_INTERFACE
    def get(self):
        """List all devices."""
        try:
            col = get_devices_collection()
            devices = [serialize_device(d) for d in col.find({}, {"_id": 0})]
            return devices, 200
        except PyMongoError as exc:
            return error_response(500, "InternalError", f"Database error: {exc}")
        except Exception as exc:
            return error_response(500, "InternalError", f"Unexpected error: {exc}")

    # PUBLIC_INTERFACE
    def post(self):
        """Create a new device with a unique name."""
        payload = request.get_json(silent=True)
        is_valid, errors = validate_device_create(payload)
        if not is_valid:
            return error_response(400, "BadRequest", "Invalid input", {"errors": errors})

        device = {
            "name": payload["name"].strip(),
            "ip": payload["ip"].strip(),
            "type": payload["type"],
            "location": payload["location"].strip(),
        }

        try:
            col = get_devices_collection()
            col.insert_one(device)
            return serialize_device(device), 201
        except DuplicateKeyError:
            return error_response(409, "Conflict", "Device with this name already exists")
        except PyMongoError as exc:
            return error_response(500, "InternalError", f"Database error: {exc}")
        except Exception as exc:
            return error_response(500, "InternalError", f"Unexpected error: {exc}")


class DeviceResource(Resource):
    """
    Single device resource.
    - GET /devices/<name>
    - PUT /devices/<name>
    - DELETE /devices/<name>
    """

    # PUBLIC_INTERFACE
    def get(self, name: str):
        """Get a device by name."""
        try:
            col = get_devices_collection()
            doc = col.find_one({"name": name})
            if not doc:
                return error_response(404, "NotFound", "Device not found")
            return serialize_device(doc), 200
        except PyMongoError as exc:
            return error_response(500, "InternalError", f"Database error: {exc}")
        except Exception as exc:
            return error_response(500, "InternalError", f"Unexpected error: {exc}")

    # PUBLIC_INTERFACE
    def put(self, name: str):
        """Update device by name (ip, type, location)."""
        payload = request.get_json(silent=True)
        is_valid, errors = validate_device_update(payload)
        if not is_valid:
            return error_response(400, "BadRequest", "Invalid input", {"errors": errors})

        update_fields = {
            "ip": payload["ip"].strip(),
            "type": payload["type"],
            "location": payload["location"].strip(),
        }

        try:
            col = get_devices_collection()
            res = col.find_one_and_update(
                {"name": name},
                {"$set": update_fields},
                return_document=True,
            )
            if not res:
                return error_response(404, "NotFound", "Device not found")
            # fetch updated
            doc = col.find_one({"name": name})
            return serialize_device(doc), 200
        except PyMongoError as exc:
            return error_response(500, "InternalError", f"Database error: {exc}")
        except Exception as exc:
            return error_response(500, "InternalError", f"Unexpected error: {exc}")

    # PUBLIC_INTERFACE
    def delete(self, name: str):
        """Delete device by name."""
        try:
            col = get_devices_collection()
            res = col.delete_one({"name": name})
            if res.deleted_count == 0:
                return error_response(404, "NotFound", "Device not found")
            return {"message": "Device deleted"}, 200
        except PyMongoError as exc:
            return error_response(500, "InternalError", f"Database error: {exc}")
        except Exception as exc:
            return error_response(500, "InternalError", f"Unexpected error: {exc}")


class PingResource(Resource):
    """
    Ping a device by name.
    - GET /ping/<name>
    """

    # PUBLIC_INTERFACE
    def get(self, name: str):
        """Ping the device associated with the given name and return status and timestamp."""
        try:
            col = get_devices_collection()
            doc = col.find_one({"name": name})
            if not doc:
                return error_response(404, "NotFound", "Device not found")

            ip = doc.get("ip")
            # Perform a quick ping with timeout, 1 packet for responsiveness
            try:
                resp = ping(ip, count=1, timeout=1, verbose=False)
                if resp.success():
                    status = "success"
                    details = f"Reply from {ip} in {resp.rtt_avg_ms:.2f} ms"
                else:
                    # Determine timeout vs failure from replies
                    any_reply = any(r.success for r in resp._responses)  # internal structure
                    status = "failure" if any_reply else "timeout"
                    details = "No response" if status == "timeout" else "Packet loss"
            except Exception as ping_exc:
                status = "failure"
                details = f"Ping error: {ping_exc}"

            return {
                "name": name,
                "status": status,
                "details": details,
                "timestamp": current_timestamp_iso(),
            }, 200
        except PyMongoError as exc:
            return error_response(500, "InternalError", f"Database error: {exc}")
        except Exception as exc:
            return error_response(500, "InternalError", f"Unexpected error: {exc}")
