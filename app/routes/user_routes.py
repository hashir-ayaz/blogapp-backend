# routes.py
from flask import render_template, redirect, url_for, request, jsonify
from app import app, db
from models import User


@app.route("/register", methods=["POST"])
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
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        # Return the newly created user
        return (
            jsonify(
                {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                }
            ),
            201,
        )
    return


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):

        # Implement session handling here
        print("Login Successful!")
        return jsonify({"message": "Login Successful!"}), 200
    else:
        print("Invalid email or password.")
        return jsonify({"message": "Invalid email or password."}), 401


@app.route("/users")
def get_users():
    users = User.query.all()
    return users
