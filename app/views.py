import os

from flask_login import login_required, login_user, current_user, logout_user, mixins
from werkzeug.security import check_password_hash

from app import app
from flask import request, render_template, redirect, url_for, session

from app.models import *
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def main():
    categories = Category.query.all()
    authors = Author.query.all()

    try:
        username = current_user.name
        is_login = True
    except:
        username = 'Новый пользователь'
        is_login = False

    data = {
        'username': username,
        'is_login': is_login,
        'categories': categories,
        'authors': authors
    }
    return render_template('main.html', data=data)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    message = ''

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            message = 'Пользователь с таким email уже зарегистрирован!'
        else:
            new_user = User(
                email=email,
                name=username,
                password=password
            )

            db.session.add(new_user)
            db.session.commit()

            session['data'] = {'message_reg': 'Вы успешно зарегистрировались!'}
            return redirect(url_for('.login'))

    return render_template('register.html', message=message)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if not isinstance(current_user, mixins.AnonymousUserMixin):
        return redirect(url_for('.main'))
    message_reg = ''
    try:
        message_reg = session.get('data')['message_reg']
        session.get('data')['message_reg'] = ''
    except:
        message_reg = ''

    message = ''

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or user.password != password:
            message = 'Неверный логин или пароль!'
        else:
            login_user(user)
            return redirect(url_for('.main'))

    data = {
        'message': message,
        'message_reg': message_reg
    }

    return render_template('login.html', data=data)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.main'))


# Добавить проверку на имя, автора


@app.route('/category/<int:id>')
def category_page(id):
    authors = Author.query.all()
    categories = Category.query.all()
    category = Category.query.filter_by(id=id).first()

    books = category.books
    category_name = category.name

    try:
        username = current_user.name
        is_login = True
    except:
        username = 'Новый пользователь'
        is_login = False

    data = {
        'books': books,
        "category_name": category_name,
        'categories': categories,
        'is_login': is_login,
        'username': username,
        'authors': authors,
        'category': category
    }

    return render_template('category.html', data=data)


@app.route('/book/<int:id>')
def book_page(id):
    book = Book.query.filter_by(id=id).first()
    authors = Author.query.all()
    categories = Category.query.all()

    book_text = open(book.text).read()

    try:
        username = current_user.name
        is_login = True
    except:
        username = 'Новый пользователь'
        is_login = False

    data = {
        'categories': categories,
        'book': book,
        'book_text': book_text,
        'is_login': is_login,
        'username': username,
        'authors': authors,
    }

    return render_template('book.html', data=data)


@app.route('/author/<int:id>')
def author_page(id):
    authors = Author.query.all()
    categories = Category.query.all()
    try:
        username = current_user.name
        is_login = True
    except:
        username = 'Новый пользователь'
        is_login = False

    author = Author.query.filter_by(id=id).first()

    books = author.books

    data = {
        'categories': categories,
        'is_login': is_login,
        'username': username,
        'authors': authors,
        'author': author,
        'books': books
    }

    return render_template('author.html', data=data)


@app.route('/profile/<username>')
@login_required
def profile_page(username):
    authors = Author.query.all()
    categories = Category.query.all()

    data = {
        'categories': categories,
        'is_login': True,
        'username': username,
        'authors': authors
    }


@app.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload_page():
    categories = Category.query.all()
    authors = Author.query.all()

    try:
        username = current_user.name
        is_login = True
    except:
        username = 'Новый пользователь'
        is_login = False

    message = ''

    if request.method == 'POST':
        file = request.files['file']
        author_name = request.form['author_name']
        title = request.form['title']
        category_name = request.form['category']

        category = Category.query.filter_by(name=category_name).first()
        author = Author.query.filter_by(name=author_name).first()

        if not category:
            new_category = Category(
                name=category_name
            )

            db.session.add(new_category)
            db.session.commit()

            category = Category.query.filter_by(name=category_name).first()

        if not author:
            new_author = Author(
                name=author_name
            )
            db.session.add(new_author)
            db.session.commit()

            author = Author.query.filter_by(name=author_name).first()

        author_id = author.id
        category_id = category.id

        if file and allowed_file(file.filename):
            file.filename = title
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

            book = Book(
                name=title,
                info='test info',
                text=UPLOAD_FOLDER+title,
                category_id=category_id,
                author_id=author_id,
                uploader_id=current_user.id
            )

            db.session.add(book)
            db.session.commit()
        else:
            message = 'Книга не была загружена =('

    data = {
        'is_login': is_login,
        'message': message,
        'username': username,
        'categories': categories,
        'authors': authors
    }

    return render_template('upload_page.html', data=data)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
