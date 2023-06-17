from flask import Flask
from flask_login import LoginManager

from config import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = '.login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import views
