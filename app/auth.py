from flask import Blueprint, request, jsonify, current_app
from .models import User
from . import db
from . import bcrypt
import jwt
from datetime import datetime, timedelta


auth = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email address already registered'}), 409

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # For now, we'll default the role to 'manager'. We can refine this later.
    new_user = User(
        email=data['email'],
        password_hash=hashed_password,
        name=data.get('name', 'Unnamed User'),
        role='manager'
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})
