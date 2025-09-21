import pytest
from app import create_app, db
from app.models import User, Team, TeamMembership
import uuid



def create_user(name, email):
    user = User(email=email, password_hash='pw', name=name)
    db.session.add(user)
    db.session.commit()
    return user

def test_team_crud(client):
    # Create users
    u1 = create_user('Alice', 'alice@example.com')
    u2 = create_user('Bob', 'bob@example.com')
    # Create team
    resp = client.post('/api/teams/', json={
        'name': 'Dev Team',
        'manager_id': str(u1.id),
        'members': [
            {'user_id': str(u1.id), 'summary': 'Lead'},
            {'user_id': str(u2.id), 'summary': 'Developer'}
        ]
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['name'] == 'Dev Team'
    assert data['manager_id'] == str(u1.id)
    assert len(data['members']) == 2

    team_id = data['id']
    # Get team
    resp = client.get(f'/api/teams/{team_id}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['name'] == 'Dev Team'
    # Update team
    resp = client.put(f'/api/teams/{team_id}', json={
        'name': 'QA Team',
        'manager_id': str(u2.id),
        'members': [
            {'user_id': str(u2.id), 'summary': 'QA Lead'}
        ]
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['name'] == 'QA Team'
    assert data['manager_id'] == str(u2.id)
    assert len(data['members']) == 1
    # Delete team
    resp = client.delete(f'/api/teams/{team_id}')
    assert resp.status_code == 200
    assert resp.get_json()['message'] == 'Team deleted'
