from flask import request, jsonify
from mongoengine import Document, StringField

class User(Document):
    fullName = StringField(required=True)
    email = StringField(required=True, unique=True)
    mobileNumber = StringField(required=True)
    password = StringField(required=True)
def register():
    data = request.get_json()

    if data["password"] != data["confirmPassword"]:
        return jsonify({"message": "Passwords do not match"}), 400

    if User.objects(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(
        fullName=data["fullName"],
        email=data["email"],
        mobileNumber=data["mobileNumber"],
        password=data["password"]
    )

    user.save()
    return jsonify({"message": "User registered successfully"}), 201
from flask import request, jsonify
from controllers.auth_controller import User  # or wherever your User model is

def login():
    data = request.get_json()

    identifier = data.get("identifier")  # frontend should send email OR mobileNumber
    password = data.get("password")

    if not identifier or not password:
        return jsonify({"message": "Identifier and password are required"}), 400

    # Check if a user exists with email OR mobileNumber
    user = User.objects(
        __raw__={"$or": [{"email": identifier}, {"mobileNumber": identifier}]},
        password=password
    ).first()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": str(user.id),
            "fullName": user.fullName,
            "email": user.email,
            "mobileNumber": user.mobileNumber
        }
    }), 200
