# Test Suites Summary

This document summarizes the initial test suites added for both the backend (pytest) and the frontend (Jest/RTL).

Backend (Flask, pytest)
- Location: FlaskBackend/tests/
- Files and tests:
  1) test_utils.py (6 tests)
     - validate_device_create_success_ipv4: Valid device creation payload is accepted.
     - validate_device_create_errors: Multiple validation errors are reported.
     - validate_device_update_success: Valid device update payload is accepted.
     - validate_device_update_rejects_name_change: Update payload containing 'name' is rejected.
     - serialize_device: Removes _id and returns expected fields.
     - error_response_shape_and_status_code: Ensures error response body and status are correct.
     - current_timestamp_iso_format: ISO timestamp ends with 'Z' and uses 'T' separator.
  2) test_api.py (8 tests)
     - devices_list_empty: GET /devices returns empty list.
     - create_device_success: POST /devices creates a device.
     - create_device_validation_error: Invalid POST returns 400 with errors.
     - get_device_not_found: GET /devices/{name} returns 404 for unknown device.
     - update_device_success: PUT /devices/{name} updates device fields.
     - update_device_validation_error: Invalid PUT returns 400.
     - delete_device_success: DELETE /devices/{name} returns success message.
     - ping_success: GET /ping/{name} uses pythonping and returns success.
     - ping_not_found: GET /ping/{name} returns 404 when device missing.

Frontend (React, Jest + React Testing Library)
- Location: ReactFrontend/src/
- Files and tests:
  1) App.theme.test.js (1 test)
     - toggles theme and updates aria label: Button toggles data-theme on document and aria-label changes.
  2) api.test.js (6 tests)
     - listDevices returns devices array
     - getDevice calls correct path
     - createDevice posts payload
     - updateDevice puts to correct path
     - deleteDevice returns true when status 204
     - pingDevice calls correct path

Total counts
- Backend: 14 tests
- Frontend: 7 tests
- Grand total: 21 tests

Notes
- Backend API tests mock the Mongo collection and pythonping to avoid external dependencies.
- Frontend API wrapper tests mock axios via jest.mock("axios").
