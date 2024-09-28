# models.py
from app import db
from datetime import datetime
import bcrypt


class User(db.Model):
    __tablename__ = "users"  # Optional: explicitly define table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    bio = db.Column(db.String(150), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    followers = db.Column(db.Integer, default=0)
    following = db.Column(db.Integer, default=0)
    profile_image = db.Column(db.String(150), nullable=True)
    batch = db.Column(
        db.String(10), nullable=True
    )  # make this enum (current year - current year - 7)
    department = db.Column(db.String(150), nullable=True)  # make this enum

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return f"<User {self.username}> {self.email} {self.created_at} {self.updated_at} {self.followers} {self.following} {self.profile_image} {self.batch} {self.department}"

    # Password handling
    def set_password(self, password):
        """Hashes the password and stores it."""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode(
            "utf-8"
        )

    def check_password(self, password):
        """Checks the hashed password."""
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )
