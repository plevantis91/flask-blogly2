"""Models for Blogly"""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

default_img = 'https://www.example.com/default.png'

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)
    
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
    def formatted_datetime(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')


    