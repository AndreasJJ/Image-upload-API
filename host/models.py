from host import db, login
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    storage_space = db.Column(db.Integer)
    links = db.relationship('link', backref='links', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)   

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    size = db.Column(db.Integer)

    def __repr__(self):
        return '<Link {}>'.format(self.url)