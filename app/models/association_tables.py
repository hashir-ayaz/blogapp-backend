from app import db

# Define the association table between Post and Tag
post_tag = db.Table(
    "post_tag",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)

# assocation table for bookmarks , it has user_id and post_id
bookmarks = db.Table(
    "bookmarks",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
)

# association table for likes, it has user_id and post_id
likes = db.Table(
    "likes",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
)

# assocation tables for followers, it has follower_id and following_id eg: user1 follows user2
followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("following_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)
