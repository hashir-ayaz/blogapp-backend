from flask import jsonify, request, Blueprint
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from slugify import slugify
from datetime import datetime
from app.models.post import Post, StatusOfPost  # Import StatusOfPost Enum
from app import db

post_bp = Blueprint("post_bp", __name__)


@post_bp.route("/create", methods=["POST"])
def create():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["title", "content", "author_id"]
        for field in required_fields:
            if field not in data:
                raise BadRequest(f"Missing required field: {field}")

        # Additional field type validation
        if not isinstance(data["author_id"], int):
            raise BadRequest(f"Field 'author_id' must be an integer")
        if not isinstance(data["title"], str):
            raise BadRequest(f"Field 'title' must be a string")
        if not isinstance(data["content"], str):
            raise BadRequest(f"Field 'content' must be a string")

        # Create slug from title
        slug = slugify(data["title"])

        # Check if slug is unique
        existing_post = Post.query.filter_by(slug=slug).first()
        if existing_post:
            raise BadRequest(
                "A post with a similar title already exists. Please choose a different title."
            )

        # Normalize the status to uppercase and map it to the StatusOfPost enum
        status_str = data.get("status", "DRAFT").upper()
        if status_str not in ["PUBLISHED", "DRAFT"]:
            raise BadRequest(
                f"Invalid status: {status_str}. Must be 'PUBLISHED' or 'DRAFT'."
            )
        status_enum = (
            StatusOfPost.PUBLISHED if status_str == "PUBLISHED" else StatusOfPost.DRAFT
        )

        # Create new post
        new_post = Post(
            title=data["title"],
            content=data["content"],
            author_id=data["author_id"],
            slug=slug,
            status=status_enum,  # Use the StatusOfPost enum
            likes=data.get("likes", 0),  # Default to 0 if not provided
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Save the new post to the database
        db.session.add(new_post)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Post created successfully!",
                    "post": {
                        "id": new_post.id,
                        "title": new_post.title,
                        "slug": new_post.slug,
                        "content": new_post.content,
                        "author_id": new_post.author_id,
                        "status": new_post.status.value,  # Return string representation of status
                        "likes": new_post.likes,
                        "created_at": new_post.created_at.isoformat(),
                        "updated_at": new_post.updated_at.isoformat(),
                    },
                }
            ),
            201,
        )

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400

    except IntegrityError as e:
        db.session.rollback()
        return (
            jsonify({"error": "A database integrity error occurred: " + str(e.orig)}),
            409,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "A database error occurred: " + str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
