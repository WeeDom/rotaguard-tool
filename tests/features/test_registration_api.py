import pytest
def test_register_success(client):
	payload = {
		"email": "newuser@example.com",
		"password": "securepass",
		"name": "New User"
	}
	response = client.post("/api/auth/register", json=payload)
	assert response.status_code == 201

def test_register_duplicate_email(client):
	payload = {
		"email": "newuser@example.com",
		"password": "securepass",
		"name": "New User"
	}
	client.post("/api/auth/register", json=payload)
	response = client.post("/api/auth/register", json=payload)
	assert response.status_code == 409
	assert "already registered" in response.json["message"].lower()

def test_register_missing_fields(client):
	payload = {"email": "missing@example.com"}
	response = client.post("/api/auth/register", json=payload)
	assert response.status_code == 400
