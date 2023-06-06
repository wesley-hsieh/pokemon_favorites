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
    teams = db.relationship('Team', secondary='user_teams', backref="user")
    saved_teams = db.relationship('Team', secondary='saved_teams', backref="user_saved")

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
    health_stat = db.Column(db.Integer)
    attack_stat = db.Column(db.Integer)
    defence_stat = db.Column(db.Integer)
    special_atk_stat = db.Column(db.Integer)
    special_def_stat = db.Column(db.Integer)
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
    __table_args__ = (db.UniqueConstraint('user_id', 'pokemon_id'),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))

    user = db.relationship('User', backref="favorite")
    pokemon = db.relationship('Pokemon', backref="favorite")

class User_teams(db.Model):
    __tablename__ = "user_teams"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    user = db.relationship('User', backref="user_teams")
    team = db.relationship('Team', backref="user_teams")

class Team(db.Model):
    __tablename__ = "teams"

    #Pokemon do not need to be unique (add docstring)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_pokemon_1 = db.Column(db.Integer, db.ForeignKey('team_pokemon.id'))
    team_pokemon_2 = db.Column(db.Integer, db.ForeignKey('team_pokemon.id'))
    team_pokemon_3 = db.Column(db.Integer, db.ForeignKey('team_pokemon.id'))
    team_pokemon_4 = db.Column(db.Integer, db.ForeignKey('team_pokemon.id'))
    team_pokemon_5 = db.Column(db.Integer, db.ForeignKey('team_pokemon.id'))
    team_pokemon_6 = db.Column(db.Integer, db.ForeignKey('team_pokemon.id'))

    pokemon1 = db.relationship('Team_pokemon', foreign_keys=[team_pokemon_1])
    pokemon2 = db.relationship('Team_pokemon', foreign_keys=[team_pokemon_2])
    pokemon3 = db.relationship('Team_pokemon', foreign_keys=[team_pokemon_3])
    pokemon4 = db.relationship('Team_pokemon', foreign_keys=[team_pokemon_4])
    pokemon5 = db.relationship('Team_pokemon', foreign_keys=[team_pokemon_5])
    pokemon6 = db.relationship('Team_pokemon', foreign_keys=[team_pokemon_6])


class Team_pokemon(db.Model):
    __tablename__ = "team_pokemon"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))
    move_1 = db.Column(db.Integer, db.ForeignKey('moves.id'))
    move_2 = db.Column(db.Integer, db.ForeignKey('moves.id'))
    move_3 = db.Column(db.Integer, db.ForeignKey('moves.id'))
    move_4 = db.Column(db.Integer, db.ForeignKey('moves.id'))
    ability = db.Column(db.Text)
    ability_desc = db.Column(db.Text)
    held_item = db.Column(db.Integer, db.ForeignKey("held_items.id"))

    pokemon = db.relationship('Pokemon', backref="team_pokemon")
    move1 = db.relationship('Move', foreign_keys=[move_1])
    move2 = db.relationship('Move', foreign_keys=[move_2])
    move3 = db.relationship('Move', foreign_keys=[move_3])
    move4 = db.relationship('Move', foreign_keys=[move_4])

    held_items = db.relationship('Held_item', backref="team_pokemon")

class Held_item(db.Model):
    __tablename__ = "held_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    desc = db.Column(db.Text, nullable=False)
    sprites = db.Column(db.Text)

class Move(db.Model):
    __tablename__ = "moves"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    power = db.Column(db.Integer)
    damage_class = db.Column(db.Text)
    accuracy = db.Column(db.Integer)
    type = db.Column(db.Text)
    desc = db.Column(db.Text)

    def setDesc(self, desc):
        self.desc = desc

class Saved_teams(db.Model):
    __tablename__ = "saved_teams"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

# class Ability(db.Model):
#     __tablename__ = "abilities"
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.Text, nullable=False)
#     desc = db.Column(db.Text)

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)