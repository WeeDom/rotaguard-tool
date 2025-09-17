import pytest
def test_login_success(client):
	# Register user first
	payload = {
		"email": "loginuser@example.com",
		"password": "loginpass",
		"name": "Login User"
	}
	client.post("/api/auth/register", json=payload)
	login_payload = {
		"email": "loginuser@example.com",
		"password": "loginpass"
	}
	response = client.post("/api/auth/login", json=login_payload)
	assert response.status_code == 200
	assert "token" in response.json

def test_login_failure(client):
	login_payload = {
		"email": "wronguser@example.com",
		"password": "wrongpass"
	}
	response = client.post("/api/auth/login", json=login_payload)
	assert response.status_code == 401

def test_login_missing_fields(client):
	login_payload = {"email": "loginuser@example.com"}
	response = client.post("/api/auth/login", json=login_payload)
	assert response.status_code == 400