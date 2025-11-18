import pytest

from app.utils import (
    validate_device_create,
    validate_device_update,
    serialize_device,
    error_response,
    current_timestamp_iso,
)


def test_validate_device_create_success_ipv4():
    payload = {
        "name": "r1",
        "ip": "192.168.1.10",
        "type": "Router",
        "location": "rack-a",
    }
    ok, errors = validate_device_create(payload)
    assert ok is True
    assert errors == {}


def test_validate_device_create_errors():
    # Invalid payload with multiple issues
    payload = {
        "name": "   ",
        "ip": "999.999.1.1",
        "type": "Unknown",
        "location": "",
    }
    ok, errors = validate_device_create(payload)
    assert not ok
    # Ensure each field reports an error
    assert "name" in errors
    assert "ip" in errors
    assert "type" in errors
    assert "location" in errors


def test_validate_device_update_success():
    payload = {
        "ip": "10.0.0.5",
        "type": "Server",
        "location": "dc-1",
    }
    ok, errors = validate_device_update(payload)
    assert ok is True
    assert errors == {}


def test_validate_device_update_rejects_name_change():
    payload = {
        "ip": "10.0.0.5",
        "type": "Server",
        "location": "dc-1",
        "name": "newname",
    }
    ok, errors = validate_device_update(payload)
    assert not ok
    assert "name" in errors


def test_serialize_device():
    doc = {"name": "n1", "ip": "1.1.1.1", "type": "Switch", "location": "lab", "_id": "X"}
    ser = serialize_device(doc)
    assert ser == {"name": "n1", "ip": "1.1.1.1", "type": "Switch", "location": "lab"}
    # _id must not be present
    assert "_id" not in ser


def test_error_response_shape_and_status_code():
    body, status = error_response(404, "NotFound", "Device not found", {"extra": "v"})
    assert status == 404
    assert body["error"] == "NotFound"
    assert body["message"] == "Device not found"
    assert body["extra"] == "v"


def test_current_timestamp_iso_format():
    ts = current_timestamp_iso()
    # Basic expectations for ISO format with Z suffix
    assert ts.endswith("Z")
    # Ensure it's parseable by splitting date/time
    assert "T" in ts
