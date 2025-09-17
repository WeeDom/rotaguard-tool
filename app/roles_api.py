from .api import api
from flask_restx import Namespace, Resource, fields
from .models import Role, User
from . import db
from flask import request
import uuid
from http import HTTPStatus

ns = Namespace('roles', description='Role management operations')
api.add_namespace(ns)

role_model = ns.model('Role', {
    'id': fields.String(readonly=True, description='The role unique identifier'),
    'human_id': fields.Integer(readonly=True, description='The role human-readable unique identifier'),
    'name': fields.String(required=True, description='The role name')
})

@ns.route('/')
class RoleList(Resource):
    @ns.marshal_list_with(role_model)
    def get(self):
        """List all roles"""
        return Role.query.all()

    @ns.expect(role_model)
    @ns.marshal_with(role_model)
    def post(self):
        """Create a new role"""
        data = request.get_json()
        if not data or 'name' not in data:
            ns.abort(400, "Invalid payload or missing 'name' field.")

        new_role = Role(
            name=data['name']
        )
        db.session.add(new_role)
        db.session.commit()
        return new_role

@ns.route('/<string:id>')
@ns.response(404, 'Role not found')
@ns.param('id', 'The role identifier')
class RoleResource(Resource):
    @ns.marshal_with(role_model)
    def get(self, id):
        """Fetch a role given its identifier"""
        role_uuid = None
        try:
            role_uuid = uuid.UUID(id)
        except ValueError:
            ns.abort(400, f"Invalid id format: '{id}' is not a valid UUID.")

        # role = Role.query.get(role_uuid)
        role = db.session.get(Role, role_uuid)  # SQLAlchemy 2.0 style

        if not role:
            ns.abort(404, f"Role with id {id} not found")
        return role
