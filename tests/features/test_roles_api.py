import pytest
import uuid
def test_get_roles_empty(client):
	response = client.get("/api/roles/")
	assert response.status_code == 200
	assert response.json == []

def test_create_role(client):
	payload = {"name": "Admin"}
	response = client.post("/api/roles/", json=payload)
	assert response.status_code == 200
	assert response.json["name"] == "Admin"
	assert "id" in response.json

def test_get_role_by_id(client):
	payload = {"name": "Manager"}
	create_resp = client.post("/api/roles/", json=payload)
	role_id = create_resp.json["id"]
	response = client.get(f"/api/roles/{role_id}")
	assert response.status_code == 200
	assert response.json["name"] == "Manager"

def test_get_role_invalid_id(client):
	response = client.get("/api/roles/not-a-uuid")
	assert response.status_code == 400

def test_create_role_missing_name(client):
	payload = {}
	response = client.post("/api/roles/", json=payload)
	assert response.status_code == 400
