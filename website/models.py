from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    passward = db.Column(db.String(150))
    fname = db.Column(db.String(150))
    user_img = db.Column(db.String(150))
    notes = db.relationship('Note', backref='user')
class Note(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default= func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))