from flask_restx import Namespace, Resource, fields
from flask import request
from app.db import db
from app.models import User, Role

api = Namespace('users', description='User management')

assign_roles_model = api.model('AssignRoles', {
    'role_names': fields.List(fields.String, required=True, description='List of role names to assign')
})

role_model = api.model('Role', {
    'id': fields.String(readonly=True, description='The role unique identifier'),
    'name': fields.String(required=True, description='The role name')
})

@api.route('/<string:user_id>/roles')
class UserRoleAssignmentResource(Resource):
    @api.marshal_list_with(role_model)
    def get(self, user_id):
        """Get all roles assigned to a user"""
        user = User.query.get_or_404(user_id)
        return list(user.roles)

    @api.expect(assign_roles_model)
    def put(self, user_id):
        """Assign roles to a user (manager only)"""
        data = request.json
        role_names = data.get('role_names', [])
        user = User.query.get_or_404(user_id)
        roles = Role.query.filter(Role.name.in_(role_names)).all()
        if len(roles) != len(role_names):
            return {'message': 'One or more roles not found'}, 400
        # Remove all current roles
        user.role_associations.clear()
        from app.models import UserRole
        for role in roles:
            user_role = UserRole()
            user_role.user = user
            user_role.role = role
            db.session.add(user_role)
        db.session.commit()
        return {'message': 'Roles updated successfully'}
