"""Models for Blogly"""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

default_img = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"
class User(db.Model):
    """User"""
    __tablename__ = "users"
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default = default_img)

    posts = db.relationship("Post", backref= "user", cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, image_url=None):
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<User {self.full_name()}>"
    
class Post(db.Model):
    """Post"""
    __tablename__ = "posts"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, 
                          default = datetime.datetime.now,
                          nullable = False)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        nullable=False)
    @property
    def readable_datetime(self):
        return self.create_at.strftime("%a %b %-d %Y, %-I:%M %p")

class Tag(db.Model):
    """Tag"""
    __tablename__ = "tags"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship("Post", secondary="posts_tags", backref="tags")

class PostTag(db.Model):
    """PostTag"""
    __tablename__ = "posts_tags"
    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), 
                        primary_key=True)
    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.id'), 
                       primary_key=True)
    
def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)