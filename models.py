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

    favorites = db.relationship('Pokemon', secondary='favorites', backref='user')
    teams = db.relationship('Team', secondary="teams_tables", backref="user")

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

class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dex_number = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.Text, nullable=False)
    sprites = db.Column(db.Text)
    shiny_sprites = db.Column(db.Text)
    hp_stat = db.Column(db.Integer)
    atk_stat = db.Column(db.Integer)
    def_stat = db.Column(db.Integer)
    spatk_stat = db.Column(db.Integer)
    spdef_stat = db.Column(db.Integer)
    speed_stat = db.Column(db.Integer)
    type_1 = db.Column(db.Text, nullable=False)
    type_2 = db.Column(db.Text)

    def setTypes(self, types):
        self.type_1 = types[0]

        try:
            self.type_2 = types[1]
        except:
            pass

class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))

    user = db.relationship('User', backref="favorite")
    pokemon = db.relationship('Pokemon', backref="favorite")

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)