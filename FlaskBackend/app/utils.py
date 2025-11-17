from typing import Dict, Any, Tuple
from datetime import datetime
import ipaddress


ALLOWED_TYPES = {"Router", "Switch", "Server"}


# PUBLIC_INTERFACE
def validate_device_create(payload: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
    """
    Validate request payload for device creation.
    Required fields: name(str), ip(str, IPv4/IPv6), type(enum), location(str)
    Returns:
        (is_valid, errors_dict)
    """
    errors: Dict[str, str] = {}

    if not isinstance(payload, dict):
        return False, {"body": "Invalid JSON body"}

    # name
    name = payload.get("name")
    if not isinstance(name, str) or not name.strip():
        errors["name"] = "name is required and must be a non-empty string"

    # ip
    ip = payload.get("ip")
    if not isinstance(ip, str) or not ip.strip():
        errors["ip"] = "ip is required and must be a non-empty string"
    else:
        if not _is_valid_ip(ip.strip()):
            errors["ip"] = "ip must be a valid IPv4/IPv6 address"

    # type
    dev_type = payload.get("type")
    if not isinstance(dev_type, str) or dev_type not in ALLOWED_TYPES:
        errors["type"] = f"type must be one of {sorted(ALLOWED_TYPES)}"

    # location
    location = payload.get("location")
    if not isinstance(location, str) or not location.strip():
        errors["location"] = "location is required and must be a non-empty string"

    return (len(errors) == 0), errors


# PUBLIC_INTERFACE
def validate_device_update(payload: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
    """
    Validate request payload for device update.
    Required fields: ip, type, location (same rules as create, but name is path param and not updatable)
    Returns:
        (is_valid, errors_dict)
    """
    errors: Dict[str, str] = {}

    if not isinstance(payload, dict):
        return False, {"body": "Invalid JSON body"}

    # ip
    ip = payload.get("ip")
    if not isinstance(ip, str) or not ip.strip():
        errors["ip"] = "ip is required and must be a non-empty string"
    else:
        if not _is_valid_ip(ip.strip()):
            errors["ip"] = "ip must be a valid IPv4/IPv6 address"

    # type
    dev_type = payload.get("type")
    if not isinstance(dev_type, str) or dev_type not in ALLOWED_TYPES:
        errors["type"] = f"type must be one of {sorted(ALLOWED_TYPES)}"

    # location
    location = payload.get("location")
    if not isinstance(location, str) or not location.strip():
        errors["location"] = "location is required and must be a non-empty string"

    # name change not allowed
    if "name" in payload:
        errors["name"] = "name cannot be updated"

    return (len(errors) == 0), errors


# PUBLIC_INTERFACE
def serialize_device(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a MongoDB device document to API schema object by removing _id and returning required fields.
    """
    return {
        "name": doc.get("name"),
        "ip": doc.get("ip"),
        "type": doc.get("type"),
        "location": doc.get("location"),
    }


# PUBLIC_INTERFACE
def error_response(status: int, error: str, message: str, extra: Dict[str, Any] | None = None):
    """
    Consistent JSON error response structure.
    """
    body: Dict[str, Any] = {"error": error, "message": message}
    if extra:
        body.update(extra)
    return body, status


def _is_valid_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except Exception:
        return False


# PUBLIC_INTERFACE
def current_timestamp_iso() -> str:
    """Return current UTC timestamp in ISO 8601 format with Z suffix."""
    return datetime.utcnow().isoformat() + "Z"
