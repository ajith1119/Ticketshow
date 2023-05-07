from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

current_dir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir,"ticket2.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
