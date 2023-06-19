"""Seed database with sample data from API"""

from app import db
from models import User, Pokemon, Favorite, Team, Team_pokemon, Held_item, Move

from string import Template
import requests

from helper import createUser, queryPokemonByNameOrId, queryPokemonMoves, createMove, queryAbilityDesc, createTeamPokemon, createTeam, createUserTeams, createAllItems

"""Run this file first"""

db.drop_all()
db.create_all()

print("populate users")

try:
    createUser("red", "password", "champion@email.com")
    createUser("brock", "pasword", "rocksaregreat@email.com")
    createUser("misty", "password", "waterisbetterdummy@email.com")
    createUser("sabrina", "password", "ghostsaremyfriend@email.com")
    createUser("admin", "admin", "admin@adminemail.com")
except:
    db.session.rollback()

print("populate pokemon")
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
    pokemon_id = 8,
    shiny = True
)

try:
    db.session.add_all([brock_fav, red_fav1, red_fav2, red_fav3, red_fav4, red_fav5, red_fav6, red_fav7])
    db.session.commit()
except:
    db.session.rollback()

#populate held_item table
print("populate held items")
createAllItems()

#create example user teams

#create team_pokemon and commit
print("populate team")
red_pikachu = createTeamPokemon("pikachu", "charm", "quick attack", "thunderbolt", "thunder", "static", "light ball")
red_blastoise = createTeamPokemon("blastoise", "blizzard", "hydro cannon", "flash cannon", "focus blast", "torrent", "mystic water")
red_charizard = createTeamPokemon("charizard", "blast burn", "flare blitz", "dragon pulse", "air slash", "blaze", "charcoal")
red_venusaur = createTeamPokemon("venusaur", "frenzy plant", "giga drain", "sludge bomb", "sleep powder", "overgrow", "miracle seed")
red_snorlax = createTeamPokemon("snorlax", "shadow ball", "crunch", "blizzard", "giga impact", "thick fat", "leftoevers")
red_lapras = createTeamPokemon("lapras", "body slam", "brine", "blizzard", "psychic", "shell armor", None)
db.session.add_all([red_pikachu, red_blastoise, red_charizard, red_lapras, red_snorlax, red_venusaur])
db.session.commit()

#create the Team and commit
red_team = createTeam(1, "HGSS Mt.Silver", red_pikachu, red_blastoise, red_charizard, red_venusaur, red_lapras, red_snorlax)
db.session.add(red_team)
db.session.commit()




