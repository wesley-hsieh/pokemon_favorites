from models import User, Pokemon, Favorite
import requests

getPokemonURL = "https://pokeapi.co/api/v2/pokemon/"

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
    #set Pokemon Types separately to take into account both a singular type and multiple.
    queriedPokemon.setTypes(types)

    return queriedPokemon