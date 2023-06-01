"""Seed database with sample data from CSV Files."""

from app import db
from models import User, Pokemon, Favorite
from helper import queryPokemonByNameOrId

import requests

db.drop_all()
db.create_all()

red = User.register(
    username="red",
    pwd="password",
    email="champion@email.com"
)

brock = User.register(
    username="brock",
    pwd="password",
    email="rocksaregreat@email.com"
)

misty = User.register(
    username="misty",
    pwd="password",
    email="waterisbetterdummy@email.com"
)

sabrina = User.register(
    username="sabrina",
    pwd="password",
    email="ghostsaremyfriend@email.com"
)

geodude = queryPokemonByNameOrId("geodude")

# pikachu = queryPokemonByNameOrId("pikachu")
# blastoise = queryPokemonByNameOrId("blastoise")
# venusaur = queryPokemonByNameOrId("venusaur")
# charizard = queryPokemonByNameOrId("charizard")
# espeon = queryPokemonByNameOrId("espeon")
# snorlax = queryPokemonByNameOrId("snorlax")

brock_fav = Favorite(
    user_id = 2,
    pokemon_id = 1
)

db.session.add_all([red, brock, misty, sabrina, geodude, brock_fav])
# db.session.add_all([pikachu, blastoise, venusaur, charizard, espeon, snorlax])

db.session.commit()
