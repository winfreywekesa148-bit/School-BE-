from flask import Blueprint, request, jsonify
from models import User
from extensions import db

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    name = data.get('name')
    full_name = data.get('full_name')
    role = data.get('role', 'student')
    
    if not username or not password or not email:
        return jsonify({'message': 'Username, password, and email are required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 409
    
    user = User(
        username=username,
        name=name or username,
        full_name=full_name or name,
        email=email,
        role=role
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201
