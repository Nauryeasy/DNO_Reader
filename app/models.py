from datetime import datetime

from app import db
from flask_login import UserMixin


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    books = db.relationship('Book', backref='category')


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    books = db.relationship('Book', backref='author')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    upload_books = db.relationship('Book', backref='uploader')
    comments = db.relationship('Comment', backref='author')


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    info = db.Column(db.Text(), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    author_id = db.Column(db.Integer(), db.ForeignKey('authors.id'))
    uploader_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='book')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer(), db.ForeignKey('books.id'))
