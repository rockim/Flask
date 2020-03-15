from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __table_name__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    findpassword = db.Column(db.String(80))
    def __init__(self, username, userid, email, password):
        self.username = username
        self.userid = userid
        self.email = email
        self.set_password(password)
        self.findpassword = password

    def __repr__(self):
        return f"<User( '{self.id}', '{self.username}', '{self.userid}', '{self.email}','{self.findpassword}')>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)
