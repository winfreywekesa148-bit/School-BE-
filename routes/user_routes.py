from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from extensions import db
from models import User

user_bp = Blueprint("user_bp", __name__)


# ------------------------
# Register
# ------------------------
@user_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    # Check if email already exists
    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({
            "message": "Email already exists."
        }), 400

    # Create new user
    user = User(
        username=data["username"],
        name=data["name"],
        full_name=data["full_name"],
        email=data["email"],
        role=data["role"]
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful."
    }), 201


# ------------------------
# Login
# ------------------------
@user_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if user is None:
        return jsonify({
            "message": "User not found."
        }), 404

    if not user.check_password(data["password"]):
        return jsonify({
            "message": "Incorrect password."
        }), 401

    token = create_access_token(identity=user.user_id)

    return jsonify({
        "token": token,
        "role": user.role,
        "username": user.username,
        "message": "Login Successful"
    }), 200


# ------------------------
# Get All Users
# ------------------------
@user_bp.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    results = []

    for user in users:

        results.append({
            "id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        })

    return jsonify(results), 200


# ------------------------
# Delete User
# ------------------------
@user_bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):

    user = User.query.get(id)

    if user is None:
        return jsonify({
            "message": "User not found."
        }), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "User deleted."
    }), 200