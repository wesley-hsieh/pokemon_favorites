"""Seed database with sample data from API"""

from app import db
from models import User, Pokemon, Favorite, User_teams, Team, Team_pokemon, Held_item, Move

from string import Template
import requests

from helper import createUser, queryPokemonByNameOrId, queryPokemonMoves, createMove, queryAbilityDesc, createTeamPokemon, createTeam, createUserTeams, createAllItems

"""Run this file first"""

db.drop_all()
db.create_all()

try:
    createUser("red", "password", "champion@email.com")
    createUser("brock", "pasword", "rocksaregreat@email.com")
    createUser("misty", "password", "waterisbetterdummy@email.com")
    createUser("sabrina", "password", "ghostsaremyfriend@email.com")
except:
    db.session.rollback()

geodude = queryPokemonByNameOrId("geodude")
pikachu = queryPokemonByNameOrId("pikachu")
blastoise = queryPokemonByNameOrId("blastoise")
venusaur = queryPokemonByNameOrId("venusaur")
charizard = queryPokemonByNameOrId("charizard")
espeon = queryPokemonByNameOrId("espeon")
snorlax = queryPokemonByNameOrId("snorlax")
lapras = queryPokemonByNameOrId("lapras")

try:
    db.session.add_all([geodude, pikachu, blastoise, venusaur, charizard, espeon, snorlax, lapras])
    db.session.commit()
except:
    db.session.rollback()

brock_fav = Favorite(
    user_id = 2,
    pokemon_id = 1
)

red_fav1 = Favorite(
    user_id = 1,
    pokemon_id = 2
)

red_fav2 = Favorite(
    user_id = 1,
    pokemon_id = 3
)

red_fav3 = Favorite(
    user_id = 1,
    pokemon_id = 4
)

red_fav4 = Favorite(
    user_id = 1,
    pokemon_id = 5
)

red_fav5 = Favorite(
    user_id = 1,
    pokemon_id = 6
)

red_fav6 = Favorite(
    user_id = 1,
    pokemon_id = 7
)

red_fav7 = Favorite(
    user_id = 1,
    pokemon_id = 8
)

try:
    db.session.add_all([brock_fav, red_fav1, red_fav2, red_fav3, red_fav4, red_fav5, red_fav6, red_fav7])
    db.session.commit()
except:
    db.session.rollback()

db.session.commit()
