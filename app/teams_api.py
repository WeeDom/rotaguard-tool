from .api import api
from flask_restx import Namespace, Resource, fields
from flask import request
from .models import Team, TeamMembership, User
from . import db
import uuid

ns = Namespace('teams', description='Team management operations')
api.add_namespace(ns)

team_member_model = ns.model('TeamMember', {
    'user_id': fields.String(required=True, description='User ID'),
    'summary': fields.String(description='Role summary in the team'),
})

team_model = ns.model('Team', {
    'id': fields.String(readonly=True, description='The team unique identifier'),
    'name': fields.String(required=True, description='The team name'),
    'manager_id': fields.String(description='Manager user ID'),
    'members': fields.List(fields.Nested(team_member_model)),
})

@ns.route('/')
class TeamList(Resource):
    @ns.marshal_list_with(team_model)
    def get(self):
        """List all teams"""
        return Team.query.all()

    @ns.expect(team_model)
    @ns.marshal_with(team_model)
    def post(self):
        """Create a new team"""
        data = request.get_json() or {}
        name = data.get('name')
        manager_id = data.get('manager_id')
        if not name:
            ns.abort(400, "Missing team name.")
        team = Team()
        team.name = name
        team.manager_id = manager_id
        db.session.add(team)
        db.session.commit()
        # Add members if provided
        members = data.get('members') or []
        for member in members:
            user = User.query.get(member.get('user_id'))
            if user:
                tm = TeamMembership()
                tm.user_id = user.id
                tm.team_id = team.id
                tm.summary = member.get('summary')
                db.session.add(tm)
        db.session.commit()
        return team

@ns.route('/<string:id>')
@ns.response(404, 'Team not found')
@ns.param('id', 'The team identifier')
class TeamResource(Resource):
    @ns.marshal_with(team_model)
    def get(self, id):
        """Fetch a team by ID"""
        team = Team.query.get_or_404(id)
        return team

    @ns.expect(team_model)
    @ns.marshal_with(team_model)
    def put(self, id):
        """Update a team"""
        team = Team.query.get_or_404(id)
        data = request.get_json() or {}
        if 'name' in data:
            team.name = data['name']
        if 'manager_id' in data:
            team.manager_id = data['manager_id']
        # Update members
        if data.get('members') is not None:
                TeamMembership.query.filter_by(team_id=team.id).delete(synchronize_session=False)
                db.session.expire_all()  # Clear session to avoid identity map conflicts
                for member in data['members']:
                    user = User.query.get(member.get('user_id'))
                    if user:
                        tm = TeamMembership()
                        tm.user_id = user.id
                        tm.team_id = team.id
                        tm.summary = member.get('summary')
                        db.session.add(tm)
        db.session.commit()
        return team

    def delete(self, id):
        """Delete a team"""
        team = Team.query.get_or_404(id)
        TeamMembership.query.filter_by(team_id=team.id).delete(synchronize_session=False)
        db.session.delete(team)
        db.session.commit()
        return {'message': 'Team deleted'}
