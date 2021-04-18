from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv()

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    return app

# Database
def crete_datebase(app):
    # TODO: create a remote database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:devraj@127.0.0.1:3306/database"
    app.config['SECRET_KEY'] = os.getenv('secret')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    return db

# Flask App
app = create_app()

