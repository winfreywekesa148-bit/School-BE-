"""Custom decorators for route protection and validation."""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models import User


def admin_required(fn):
    """Decorator restricting access to admin users only."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'message': 'Admin privileges required.'}), 403
        return fn(*args, **kwargs)
    return wrapper


def teacher_or_admin_required(fn):
    """Decorator restricting access to teachers and admins."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role not in ('admin', 'teacher'):
            return jsonify({'message': 'Teacher or admin privileges required.'}), 403
        return fn(*args, **kwargs)
    return wrapper
