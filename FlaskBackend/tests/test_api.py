import json
from unittest.mock import patch, MagicMock
import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def _mock_collection_with_data(initial=None):
    """Return a MagicMock that simulates a pymongo collection with basic CRUD."""
    data = {d["name"]: d.copy() for d in (initial or [])}
    col = MagicMock()

    # find
    def find(filter=None, projection=None):
        # Return list of docs, emulate projection removing _id when {"_id":0}
        res = []
        for v in data.values():
            doc = v.copy()
            if projection and projection.get("_id") == 0 and "_id" in doc:
                doc.pop("_id", None)
            res.append(doc)
        return res

    col.find.side_effect = find

    # find_one
    def find_one(query):
        name = query.get("name")
        return data.get(name)

    col.find_one.side_effect = find_one

    # insert_one
    def insert_one(doc):
        name = doc["name"]
        if name in data:
            raise Exception("DuplicateKeyError")
        data[name] = doc.copy()
        return MagicMock(inserted_id="fakeid")

    col.insert_one.side_effect = insert_one

    # find_one_and_update
    def find_one_and_update(query, update, return_document=True):
        name = query.get("name")
        if name not in data:
            return None
        for k, v in update.get("$set", {}).items():
            data[name][k] = v
        return data[name]

    col.find_one_and_update.side_effect = find_one_and_update

    # delete_one
    class _DelRes:
        deleted_count = 0

    def delete_one(query):
        name = query.get("name")
        res = _DelRes()
        if name in data:
            del data[name]
            res.deleted_count = 1
        else:
            res.deleted_count = 0
        return res

    col.delete_one.side_effect = delete_one

    # create_index no-op
    col.create_index.return_value = "uniq_name"
    return col


@patch("app.db.get_devices_collection")
def test_devices_list_empty(mock_get_col, client):
    mock_get_col.return_value = _mock_collection_with_data([])
    resp = client.get("/devices")
    assert resp.status_code == 200
    # resources.py returns a list directly
    assert resp.is_json
    assert resp.get_json() == []


@patch("app.db.get_devices_collection")
def test_create_device_success(mock_get_col, client):
    mock_get_col.return_value = _mock_collection_with_data([])
    payload = {
        "name": "edge-1",
        "ip": "192.168.0.2",
        "type": "Router",
        "location": "edge",
    }
    resp = client.post("/devices", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["name"] == "edge-1"
    assert body["ip"] == "192.168.0.2"


@patch("app.db.get_devices_collection")
def test_create_device_validation_error(mock_get_col, client):
    mock_get_col.return_value = _mock_collection_with_data([])
    payload = {"name": "", "ip": "badip", "type": "X", "location": ""}
    resp = client.post("/devices", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 400
    body = resp.get_json()
    assert body["error"] == "BadRequest"
    assert "errors" in body


@patch("app.db.get_devices_collection")
def test_get_device_not_found(mock_get_col, client):
    mock_get_col.return_value = _mock_collection_with_data([])
    resp = client.get("/devices/ghost")
    assert resp.status_code == 404
    body = resp.get_json()
    assert body["error"] == "NotFound"


@patch("app.db.get_devices_collection")
def test_update_device_success(mock_get_col, client):
    mock_get_col.return_value = _mock_collection_with_data(
        [{"name": "srv1", "ip": "10.0.0.1", "type": "Server", "location": "dc"}]
    )
    payload = {"ip": "10.0.0.9", "type": "Server", "location": "rack-3"}
    resp = client.put("/devices/srv1", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["ip"] == "10.0.0.9"
    assert body["location"] == "rack-3"


@patch("app.db.get_devices_collection")
def test_update_device_validation_error(mock_get_col, client):
    mock_get_col.return_value = _mock_collection_with_data(
        [{"name": "sw1", "ip": "10.0.0.2", "type": "Switch", "location": "dc"}]
    )
    payload = {"ip": "", "type": "X", "location": ""}
    resp = client.put("/devices/sw1", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 400
    body = resp.get_json()
    assert body["error"] == "BadRequest"


@patch("app.db.get_devices_collection")
def test_delete_device_success(mock_get_col, client):
    mock_get_col.return_value = _mock_collection_with_data(
        [{"name": "r2", "ip": "10.0.0.3", "type": "Router", "location": "lab"}]
    )
    resp = client.delete("/devices/r2")
    # resources.py returns 200 with body {"message":"Device deleted"}
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["message"].lower().startswith("device deleted")


@patch("app.db.get_devices_collection")
@patch("app.resources.ping")
def test_ping_success(mock_ping, mock_get_col, client):
    # Setup device in mock DB
    mock_get_col.return_value = _mock_collection_with_data(
        [{"name": "r1", "ip": "1.1.1.1", "type": "Router", "location": "lab"}]
    )
    # Mock pythonping response
    ping_resp = MagicMock()
    ping_resp.success.return_value = True
    ping_resp.rtt_avg_ms = 12.34
    ping_resp._responses = []
    mock_ping.return_value = ping_resp

    resp = client.get("/ping/r1")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["name"] == "r1"
    assert body["status"] == "success"
    assert "12.34" in body["details"]


@patch("app.db.get_devices_collection")
@patch("app.resources.ping")
def test_ping_not_found(mock_ping, mock_get_col, client):
    mock_get_col.return_value = _mock_collection_with_data([])
    resp = client.get("/ping/absent")
    assert resp.status_code == 404
    body = resp.get_json()
    assert body["error"] == "NotFound"
