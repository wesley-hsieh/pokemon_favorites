"""SQLAlchemy models for app"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)


    @classmethod
    def register(cls, username, pwd, email):
        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email)

    @classmethod
    def authenticate(cls, username, pwd):
        u = User.query.filter_by(username=username.first())

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)