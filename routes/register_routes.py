from flask import request, jsonify, Flask
from models import User
from extensions import db

app = Flask(__name__)

@app.route("/register", methods=["POST"])

def register():

    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message":"Email already exists"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        role=data["role"]
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registration was Successful"
    }),201

