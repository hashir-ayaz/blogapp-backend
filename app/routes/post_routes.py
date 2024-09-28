# user_routes.py
from flask import render_template, redirect, url_for, request, jsonify, Blueprint
from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token

post_bp = Blueprint("post_bp", __name__)


@post_bp.route("/hello", methods=["GET"])
def hello():
    return "Hello, World! from posts"


@post_bp.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    if request.method == "POST":
        print(request)
        title = data["title"]
        content = data["content"]
        user_id = data["user_id"]

        new_post = Post(title=title, content=content, user_id=user_id)

        db.session.add(new_post)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Post created successfully!",
                    "post": {
                        "id": new_post.id,
                        "title": new_post.title,
                        "content": new_post.content,
                        "user_id": new_post.user_id,
                    },
                }
            ),
            201,
        )
    return
