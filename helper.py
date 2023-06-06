from models import User, Pokemon, Favorite, User_teams, Team, Team_pokemon, Held_item, Move
from app import db

import requests
import json

# DROP TABLE abilities, favorites, held_items, moves, pokemon, team_pokemon, teams, user_teams, users CASCADE;

from string import Template

getPokemonURL = "https://pokeapi.co/api/v2/pokemon/"
getMoveURL = "https://pokeapi.co/api/v2/move/"
getAbilityURL = "https://pokeapi.co/api/v2/ability/"
getItemURL = "https://pokeapi.co/api/v2/item/"

def createUser(name, pwd, email):
    user = User.register(username=name, pwd = pwd, email = email)
    db.session.add(user)
    db.session.commit()

def queryPokemonByNameOrId(pokemon_name_id):
    #grab pokemon data
    request = requests.get(getPokemonURL+pokemon_name_id)
    data = request.json()

#     for key in data:
#         print(key)
    print(len(data["moves"]))

    for move in data["moves"]:
        print(move)

    #destructure the stats
    hp_data, atk_data, def_data, spatk_data, spdef_data, speed_data = data["stats"]

    #destructure the types
    type_1, *type_2 = data["types"]

    #create list of just the actual desired value for simplicity
    types = [type_1["type"]["name"]]

    #conditional statement to test if type_2 even exists
    if type_2:
        types.append(type_2[0]["type"]["name"])

    #create pokemon instance
    queriedPokemon = Pokemon(
        dex_number = data["id"],
        name = data["name"],
        sprites = data["sprites"]["front_default"],
        shiny_sprites = data["sprites"]["front_shiny"],
        hp_stat = hp_data["base_stat"],
        atk_stat = atk_data["base_stat"],
        def_stat = def_data["base_stat"],
        spatk_stat = spatk_data["base_stat"],
        spdef_stat = spdef_data["base_stat"],
        speed_stat = speed_data["base_stat"]
    )
    #setTypes separately to take into cover both a singular type and multiple.
    queriedPokemon.setTypes(types)

    return queriedPokemon