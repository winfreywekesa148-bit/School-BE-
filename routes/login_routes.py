from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User
from extensions import db

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    access_token = create_access_token(identity=user.user_id)
    return jsonify({
        'access_token': access_token,
        'user_id': user.user_id,
        'username': user.username,
        'role': user.role
    }), 200
