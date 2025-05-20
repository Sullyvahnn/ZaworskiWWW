from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, nullable=True)
    user = db.relationship("User", back_populates="blog_articles")

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    blog_articles = db.relationship("Article", back_populates="user")
    chat_messages = db.relationship('Message', back_populates="user", lazy=True)

class Message(db.Model):
    __tablename__ = 'message'
    id = db.mapped_column(db.Integer, primary_key=True)
    user_id = db.mapped_column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    username = db.mapped_column(db.String(50), nullable=False)
    content = db.mapped_column(db.String(500), nullable=False)
    created_at = db.mapped_column(db.DateTime(), nullable=False, default=datetime.now)
    modified_at = db.mapped_column(db.DateTime(), nullable=True)
    user = db.relationship("User", back_populates="chat_messages", lazy=False)

