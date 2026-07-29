from flask import request, jsonify, Flask
from flask_jwt_extended import create_access_token
from models import User

app = Flask(__name__)

@app.route("/login", methods=["POST"])

def login():
    data = request.get_json()

    email = data["email"]

    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):

        token = create_access_token(identity=str(user.id))

        return jsonify({
            "access_token": token,
            "role": user.role,
            "name": user.name

        }),200

    return jsonify({
        "message": "Wrong email address or password. Check again"
    }), 401