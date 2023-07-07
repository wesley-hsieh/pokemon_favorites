from models import User, Pokemon, Favorite, Team, Team_pokemon, Held_item, Move, Ability
from app import db

import requests
import json

import logging

from psycopg2.errors import UndefinedFunction
from sqlalchemy.exc import ProgrammingError

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
    #TODO: check if pokemon in database
    pokemonByName, pokemonByID = None, None
    try:
        pokemonByName = Pokemon.query.filter(Pokemon.name == pokemon_name_id).one_or_none()
    except (UndefinedFunction, ProgrammingError) as err:
        db.session.rollback()
        pokemonByID = Pokemon.query.filter(Pokemon.dex_number == pokemon_name_id).one_or_none()

    # "Tooltip: flash 'maybe try using the pokedex number'"

    #ternary operation to get which of the two queries evaluated to completion
    query = pokemonByName if pokemonByName else pokemonByID

    if query:
        return query
    else:
        #grab pokemon data
        request = requests.get(getPokemonURL+str(pokemon_name_id))
        data = request.json()

        #populate moves table with data(?)
        for move in data["moves"]:
            name = move["move"]["name"]

            #query for move, making sure to replace the hyphen, if it does not exist, create move
            query_count = Move.query.filter(Move.name.ilike(name.replace('-', ' '))).count()
            if query_count == 0:
                createMove(name)

        #destructure the stats
        health_data, attack_data, defence_data, special_atk_data, special_def_data, speed_data = data["stats"]

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
            health_stat = health_data["base_stat"],
            attack_stat = attack_data["base_stat"],
            defence_stat = defence_data["base_stat"],
            special_atk_stat = special_atk_data["base_stat"],
            special_def_stat = special_def_data["base_stat"],
            speed_stat = speed_data["base_stat"]
        )
        #setTypes separately to take into cover both a singular type and multiple.
        queriedPokemon.setTypes(types)

        return queriedPokemon

def queryPokemonMoves(pokemon_name_id):
    #grab pokemon data
    request = requests.get(getPokemonURL+str(pokemon_name_id))
    data = request.json()

    #create array of move names
    moves = []
    for move in data["moves"]:
        moves.append(move["move"]["name"])

#     print(moves)
    return moves

def queryAbilityDesc(ability_name):
    try:
        request = requests.get(getAbilityURL + ability_name.replace(" ", "-"))
        data = request.json()

        for entry in data["effect_entries"]:
            if entry["language"]["name"] == "en":
                return entry["short_effect"]
    except:
        print("Some error occured")

def createMove(move_name):
    request = requests.get(getMoveURL + move_name)
    data = request.json()

    queriedMove = Move(
        name = move_name.replace('-', ' '),
        power = data["power"],
        damage_class = data["damage_class"]["name"],
        accuracy = data["accuracy"],
        type = data["type"]["name"],
    )

    #check if the move effect has a "$" sign signifying string interpolation
    try:
        move_desc = data["effect_entries"][0]["short_effect"]
        if(move_desc.find("$")):
            move_desc_template = Template(data["effect_entries"][0]["short_effect"])
            queriedMove.setDesc(move_desc_template.substitute(effect_chance=data["effect_chance"]))
        else:
            queriedMove.setDesc(move_desc)
    except:
        pass

    db.session.add(queriedMove)
    db.session.commit()

def createTeamPokemon(name, move_1, move_2, move_3, move_4, ability, held_item):
    pok = Pokemon.query.filter(Pokemon.name == name).first()
#     print(pok.id)

    held_item_id = None
    try:
        held_item_id = Held_item.query.filter(Held_item.name == held_item).first().id
#         print(held_item_id)
    except:
        pass

    return Team_pokemon(
        pokemon_id = Pokemon.query.filter(Pokemon.name == name).first().id,
        move_1 = Move.query.filter(Move.name == move_1).first().id,
        move_2 = Move.query.filter(Move.name == move_2).first().id,
        move_3 = Move.query.filter(Move.name == move_3).first().id,
        move_4 = Move.query.filter(Move.name == move_4).first().id,
        ability = ability,
        ability_desc = queryAbilityDesc(ability),
        held_item = held_item_id
    )

def createTeam(id, name, pokemon_1, pokemon_2, pokemon_3, pokemon_4, pokemon_5, pokemon_6):
    return Team(
        user_id = id,
        name = name,
        team_pokemon_1 = pokemon_1.id,
        team_pokemon_2 = pokemon_2.id,
        team_pokemon_3 = pokemon_3.id,
        team_pokemon_4 = pokemon_4.id,
        team_pokemon_5 = pokemon_5.id,
        team_pokemon_6 = pokemon_6.id
    )

def createUserTeams(user_id, team_id):
    return User_teams(
        user_id = user_id,
        team_id = team_id
    )

def createAllItems():
    request = requests.get(getItemURL)
    data = request.json()
    item_count = data["count"]

    for x in range(1, item_count+1):
        try:
            request = requests.get(getItemURL+str(x))
            data = request.json()

            if (Held_item.query.filter(Held_item.name.ilike(data["name"].replace('-', ' '))).count() ==0):
                for entry in data["effect_entries"]:
                    if entry["language"]["name"] == "en":
                        item = Held_item(
                            name = data["name"].replace('-',' '),
                            desc = entry["short_effect"],
                            sprites = data["sprites"]["default"]
                        )
                db.session.add(item)
                db.session.commit()
        except:
            pass

def createAllPokemon():
    request = requests.get(getPokemonURL)
    data = request.json()
    pokemon_count = data["count"]

    print(pokemon_count)

    for x in range(1, pokemon_count+1):
        try:
            #grab individual pokemon
            request = requests.get(getPokemonURL+str(x))
            data = request.json()

            moves = ""
            #populate moves table with data
            for move in data["moves"]:
                name = move["move"]["name"]
                moves += name.replace('-',' ') + ","

                #query for move, making sure to replace the hyphen, if it does not exist, create move
                query_count = Move.query.filter(Move.name.ilike(name.replace('-', ' '))).count()
                if query_count == 0:
                    createMove(name)

            #destructure the stats
            health_data, attack_data, defence_data, special_atk_data, special_def_data, speed_data = data["stats"]

            #destructure the types
            type_1, *type_2 = data["types"]

            #create list of just the actual desired value for simplicity
            types = [type_1["type"]["name"]]

            #conditional statement to test if type_2 even exists
            if type_2:
                types.append(type_2[0]["type"]["name"])

            abilities = data["abilities"]
            ability_str = ""

            for entry in abilities:
                createAbility(entry["ability"]["name"])
                print(entry["ability"]["name"])
                ability_str += entry["ability"]["name"].replace("-"," ") + ","

            #create pokemon instance
            queriedPokemon = Pokemon(
                dex_number = data["id"],
                name = data["name"],
                sprites = data["sprites"]["front_default"],
                shiny_sprites = data["sprites"]["front_shiny"],
                health_stat = health_data["base_stat"],
                attack_stat = attack_data["base_stat"],
                defence_stat = defence_data["base_stat"],
                special_atk_stat = special_atk_data["base_stat"],
                special_def_stat = special_def_data["base_stat"],
                speed_stat = speed_data["base_stat"],
                moves = moves,
                abilities = ability_str
            )
            #setTypes separately to take into cover both a singular type and multiple.
            queriedPokemon.setTypes(types)

            db.session.add(queriedPokemon)
            db.session.commit()
        except:
            pass

def createAbility(ability_name):
    query_count = Ability.query.filter(Ability.name == ability_name.replace("-", " ")).count()
    if query_count == 0:
        try:
            request = requests.get(getAbilityURL+ability_name)
            data = request.json()

            for entry in data["effect_entries"]:
                if entry["language"]["name"] == "en":
                    newAbility = Ability(
                        name = data["name"].replace('-',' '),
                        desc = entry["short_effect"]
                    )
                    db.session.add(newAbility)
                    db.session.commit()
        except BaseException:
            print("some error occured on ", x)
            logging.exception("an exception was thrown")

#     ability_count = data["count"]
#
#     print("ability_count", ability_count)
#
#     for x in range(1, ability_count+1):
#         try:
#             request = requests.get(getAbilityURL+str(x))
#             data = request.json()
#             name = data["name"].replace('-',' ')
#             print(name)
#
#             for entry in data["effect_entries"]:
#                 if entry["language"]["name"] == "en":
# #                     print(entry["short_effect"])
#                     newAbility = Ability(
#                         name = data["name"].replace('-',' '),
#                         desc = entry["short_effect"]
#                     )
#                     db.session.add(newAbility)
#                     db.session.commit()
#         except BaseException:
#             print("some error occured on ", x)
#             logging.exception("an exception was thrown")
