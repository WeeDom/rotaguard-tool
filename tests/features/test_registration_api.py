# test_registration_api.py

import pytest

def registration_payload(email=True, password=True, name=True):
    payload = {}
    if email:
        payload['email'] = 'test@example.com'
    if password:
        payload['password'] = 'password123'
    if name:
        payload['name'] = 'Test User'
    return payload

def test_register_success(client):
    """should successfully register a new user with valid email, password, and name"""
    payload = {
        "email": "newuser@example.com",
        "password": "securepass",
        "name": "New User"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201

def test_register_duplicate_email(client):
    """should reject registration with a duplicate email address"""
    payload = {
        'email': 'dupe@example.com',
        'password': 'password123',
        'name': 'Dupe User'
    }
    # First registration should succeed
    resp1 = client.post('/api/auth/register', json=payload)
    assert resp1.status_code == 201
    # Second registration with same email should fail
    resp2 = client.post('/api/auth/register', json=payload)
    assert resp2.status_code == 409
    resp_json = resp2.get_json()
    assert "message" in resp_json or "errors" in resp_json

@pytest.mark.parametrize(
    "email,password,name,missing_field",
    [
        (False, True, True, 'missing email'),
        (True, False, True, 'missing password'),
        (True, True, False, 'missing name'),
        (False, False, True, 'missing email and password'),
        (False, True, False, 'missing email and name'),
        (True, False, False, 'missing password and name'),
        (False, False, False, 'missing all fields'),
    ],
    ids=[
        "email required",
        "password required",
        "name required",
        "email + password required",
        "email + name required",
        "password + name required",
        "all fields required"
    ]
)
def test_register_missing_fields(client, email, password, name, missing_field):
    """should return 400 when required field(s) are missing"""
    resp = client.post('/api/auth/register', json=registration_payload(email, password, name))
    assert resp.status_code == 400
    resp_json = resp.get_json()
    assert "errors" in resp_json
