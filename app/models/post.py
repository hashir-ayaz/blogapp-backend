from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

from app.models.association_tables import post_tag


class StatusOfPost(Enum):
    PUBLISHED = "PUBLISHED"
    DRAFT = "DRAFT"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(StatusOfPost), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    likes = db.Column(db.Integer, default=0)

    tags = db.relationship(
        "Tag", secondary=post_tag, backref=db.backref("posts", lazy="dynamic")
    )

    def __repr__(self):
        return f"<Post {self.title}>"
