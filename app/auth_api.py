from .api import api
from flask_restx import Namespace, Resource, fields
from .models import User
from . import db, bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app, request

ns = Namespace('auth', description='Authentication operations')
api.add_namespace(ns)

# --- API Models for Input/Output ---

user_registration_model = ns.model('UserRegistration', {
    'email': fields.String(required=True, description='The user\'s email address'),
    'password': fields.String(required=True, description='The user\'s password'),
    'name': fields.String(required=True, description='The user\'s name')
})

user_login_model = ns.model('UserLogin', {
    'email': fields.String(required=True, description='The user\'s email address'),
    'password': fields.String(required=True, description='The user\'s password')
})

token_model = ns.model('Token', {
    'token': fields.String(description='Authentication token')
})

message_model = ns.model('Message', {
    'message': fields.String(description='A message describing the result of the operation'),
    'id': fields.String(description='The ID of the newly created user')
})


# --- Resources ---

@ns.route('/register')
class RegisterResource(Resource):
    @ns.expect(user_registration_model, validate=True)
    @ns.marshal_with(message_model, code=201)
    def post(self):
        """Creates a new user."""
        data = request.get_json()

        if User.query.filter_by(email=data['email']).first():
            ns.abort(409, 'Email address already registered')

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        new_user = User(
            email=data['email'],
            password_hash=hashed_password,
            name=data.get('name')
        )
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'New user created!', 'id': str(new_user.id)}, 201

@ns.route('/login')
class LoginResource(Resource):
    @ns.expect(user_login_model, validate=True)
    @ns.marshal_with(token_model)
    def post(self):
        """Logs in a user and returns a JWT."""
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
            ns.abort(401, 'Invalid credentials')

        token = jwt.encode({
            'user_id': str(user.id),
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        return {'token': token}
