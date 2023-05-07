from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import app

db = SQLAlchemy(app)

class User( UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    tickets = db.relationship('Ticket', backref='post')


    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):   
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    


class Venue(db.Model):
   __tablename__ = "venue"
   venueid = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String, nullable=False)
   place = db.Column(db.String)
   capacity = db.Column(db.Integer)
   shows = db.relationship('Show', backref='poster')

class Show(db.Model):
    __tablename__ = "show"
    showid = db.Column(db.Integer,primary_key=True)
    showname = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)
    tag = db.Column(db.String)
    price = db.Column(db.Integer)
    showcapacity = db.Column(db.Integer)
    eshowid = db.Column(db.Integer, db.ForeignKey("venue.venueid"))

class Ticket(db.Model):
    __tablename__ = "ticket"
    ticketid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    phoneno = db.Column(db.String)
    nooftickets = db.Column(db.String)
    eticketid = db.Column(db.Integer, db.ForeignKey("show.showid"))
    euserid = db.Column(db.Integer, db.ForeignKey("user.id"))