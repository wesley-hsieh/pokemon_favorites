"""Seed database with sample data from API"""

from app import db
from models import User, Pokemon, Favorite, Team, Team_pokemon, Held_item, Move

from string import Template
import requests

from helper import createUser, queryPokemonByNameOrId, queryPokemonMoves, createMove, queryAbilityDesc, createTeamPokemon, createTeam, createUserTeams, createAllItems
from helper import createAllPokemon, createAbility

"""Run this file first"""

def with_context():
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("populate users")

        try:
            createUser("red", "password", "champion@email.com")
            createUser("brock", "pasword", "rocksaregreat@email.com")
            createUser("misty", "password", "waterisbetterdummy@email.com")
            createUser("sabrina", "password", "ghostsaremyfriend@email.com")
            createUser("admin", "admin", "admin@adminemail.com")
            createUser("anonymous","anonymous", "dummy@dummyemail.com")
        except:
            db.session.rollback()

        print("populate pokemon")
        createAllPokemon()

        brock_fav = Favorite(
            user_id = 2,
            pokemon_id = Pokemon.query.filter(Pokemon.name == "geodude").one_or_none().id
        )

        red_fav1 = Favorite(
            user_id = 1,
            pokemon_id = Pokemon.query.filter(Pokemon.name == "pikachu").one_or_none().id

        )

        red_fav2 = Favorite(
            user_id = 1,
            pokemon_id = Pokemon.query.filter(Pokemon.name == "blastoise").one_or_none().id
        )

        red_fav3 = Favorite(
            user_id = 1,
            pokemon_id = Pokemon.query.filter(Pokemon.name == "charizard").one_or_none().id
        )

        red_fav4 = Favorite(
            user_id = 1,
            pokemon_id = Pokemon.query.filter(Pokemon.name == "venusaur").one_or_none().id
        )

        red_fav5 = Favorite(
            user_id = 1,
            pokemon_id = Pokemon.query.filter(Pokemon.name == "snorlax").one_or_none().id
        )

        red_fav6 = Favorite(
            user_id = 1,
            pokemon_id = Pokemon.query.filter(Pokemon.name == "espeon").one_or_none().id
        )

        red_fav7 = Favorite(
            user_id = 1,
            pokemon_id = Pokemon.query.filter(Pokemon.name == "lapras").one_or_none().id,
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




