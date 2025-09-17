import pytest
from app import create_app, db
from app.models import User, Role
from flask import url_for



def api_create_user(client, email, name, password='pw'):
    resp = client.post('/api/auth/register', json={
        'email': email,
        'password': password,
        'name': name
    })
    assert resp.status_code == 201
    return resp.get_json()['id']

def api_create_role(client, name):
    resp = client.post('/api/roles/', json={'name': name})
    assert resp.status_code == 200 or resp.status_code == 201
    return resp.get_json()['id']

def test_manager_can_assign_roles(client):
    manager_id = api_create_user(client, 'manager@example.com', 'Manager')
    user_id = api_create_user(client, 'user@example.com', 'User')
    api_create_role(client, 'Cashier')
    api_create_role(client, 'Chef')
    # Simulate manager assigning roles to user
    response = client.put(f'/api/users/{user_id}/roles', json={
        'role_names': ['Cashier', 'Chef']
    })
    assert response.status_code == 200

def test_assign_roles_invalid_role(client):
    manager_id = api_create_user(client, 'manager2@example.com', 'Manager2')
    user_id = api_create_user(client, 'user2@example.com', 'User2')
    api_create_role(client, 'Cashier')
    # Try to assign a non-existent role
    response = client.put(f'/api/users/{user_id}/roles', json={
        'role_names': ['Cashier', 'NonExistent']
    })
    assert response.status_code == 400
    assert b'not found' in response.data

def test_get_user_roles(client):
    manager_id = api_create_user(client, 'manager3@example.com', 'Manager3')
    user_id = api_create_user(client, 'user3@example.com', 'User3')
    api_create_role(client, 'Cashier')
    api_create_role(client, 'Chef')
    # Assign roles
    response = client.put(f'/api/users/{user_id}/roles', json={
        'role_names': ['Cashier', 'Chef']
    })
    assert response.status_code == 200
    # Retrieve roles
    response = client.get(f'/api/users/{user_id}/roles')
    assert response.status_code == 200
    data = response.get_json()
    role_names = {role['name'] for role in data}
    assert role_names == {'Cashier', 'Chef'}

def test_get_user_roles_empty(client):
    user_id = api_create_user(client, 'user5@example.com', 'User4')
    response = client.get(f'/api/users/{user_id}/roles')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []
