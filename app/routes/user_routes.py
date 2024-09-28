# user_routes.py
from flask import render_template, redirect, url_for, request, jsonify, Blueprint
from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/hello", methods=["GET"])
def hello():
    return "Hello, World!"


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if request.method == "POST":
        print(request)
        username = data["username"]
        email = data["email"]
        password = data["password"]

        # Check if user exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            print("Username or email already exists.")
            return jsonify({"message": "Username or email already exists."}), 400

        # Create new user
        new_user = User(username=username, email=email, password=password)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)
        # Return the newly created user
        return (
            jsonify(
                {
                    "message": "User created successfully!",
                    "access_token": access_token,
                    "user": {
                        "id": new_user.id,
                        "username": new_user.username,
                        "email": new_user.email,
                    },
                }
            ),
            201,
        )
    return


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):

        # Implement session handling here
        print("Login Successful!")
        access_token = create_access_token(identity=user.id)

        return (
            jsonify(
                {
                    "message": "Login Successful!",
                    "access_token": access_token,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                }
            ),
            200,
        )
    else:
        print("Invalid email or password.")
        return jsonify({"message": "Invalid email or password."}), 401


@jwt_required
@user_bp.route("/users")
def get_users():
    users = User.query.all()
    return users
