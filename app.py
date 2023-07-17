import os

from flask import Flask, render_template, request, flash, redirect, session, g, send_file
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import copy


from models import db, connect_db, User, Pokemon, Favorite, Team, Team_pokemon, Held_item, Move, Saved_teams, Ability
from forms import UserAddForm, LoginForm, PokemonForm
from helper import queryPokemonByNameOrId, queryPokemonMoves, createMove, queryAbilityDesc, createTeamPokemon, createTeam, createUserTeams, createAllItems

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///pokemon-favorites'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def homepage():
    '''Route for homepage '''

    users = User.query.all()
    teams = Team.query.all()
    return render_template("index.html", users = users, teams=teams)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id
    print(session[CURR_USER_KEY])

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        print("valid form")
        user = User.authenticate(form.username.data,
                                 form.password.data)

        print('user')
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                pwd=form.password.data,
                email=form.email.data,
            )
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

@app.route('/teams/<int:team_id>', methods=["GET", "POST"])
def display_team(team_id):
    '''Route to display a team'''
    team = Team.query.get_or_404(team_id)

    print(team)
    return render_template("/team.html", team=team)

@app.route('/teams/edit/<int:team_id>', methods=["GET", "POST"])
def edit_team(team_id):
    '''Specific route for editing a team'''
    team = Team.query.get_or_404(team_id)
    team_pokemon = [team.pokemon1, team.pokemon2, team.pokemon3, team.pokemon4, team.pokemon5, team.pokemon6]

    return render_template("team_edit.html", team = team , team_pokemon = team_pokemon)

@app.route('/teams/edit/<int:team_id>/<int:team_slot>', methods=["GET"])
def edit_team_pokemon(team_id, team_slot):
    '''Route to edit a pokemon or an entry on a team'''
    team = Team.query.get_or_404(team_id)

    pokemon = [team.pokemon1, team.pokemon2, team.pokemon3, team.pokemon4, team.pokemon5, team.pokemon6]
    team_pokemon = pokemon[team_slot - 1]

    all_pokemon = [pokemon.asDict() for pokemon in Pokemon.query.all()]
    all_items = [item.name for item in Held_item.query.all()]

    if(team_pokemon.pokemon):
        all_moves = Pokemon.query.filter(Pokemon.dex_number == team_pokemon.pokemon_id).one_or_none().moves.split(",")
        all_abilities = Pokemon.query.filter(Pokemon.dex_number == team_pokemon.pokemon_id).one_or_none().abilities.split(",")

        return render_template("pokemon_edit.html", team = team, team_pokemon = team_pokemon, allPokemon = all_pokemon, allMoves = all_moves, allAbilities = all_abilities, allItems = all_items)
    else:
        return render_template("pokemon_edit.html", team = team, team_pokemon = team_pokemon, allPokemon = all_pokemon, allItems = all_items)


@app.route("/teams/save/<int:team_id>/<int:pokemon_id>", methods=["POST"])
def save_team_state(team_id, pokemon_id):
    '''Route to actually "push" or save the changes made to the Postgresql database'''
    pokemon_name = request.form.get("pokemon")
    move_1 = request.form.get("move_1")
    move_2 = request.form.get("move_2")
    move_3 = request.form.get("move_3")
    move_4 = request.form.get("move_4")
    held_item = request.form.get("held_item")
    ability = request.form.get("ability")

    #id of the team pokemon to edit.
    team_pokemon_id = request.form.get("team_pokemon_id")

    team_pokemon = Team_pokemon.query.get_or_404(pokemon_id)

    team_pokemon.pokemon_id = Pokemon.query.filter(Pokemon.name == pokemon_name).one_or_none().id
    team_pokemon.move_1 = Move.query.filter(Move.name == move_1).one_or_none().id
    team_pokemon.move_2 = Move.query.filter(Move.name == move_2).one_or_none().id
    team_pokemon.move_3 = Move.query.filter(Move.name == move_3).one_or_none().id
    team_pokemon.move_4 = Move.query.filter(Move.name == move_4).one_or_none().id
    team_pokemon.ability = Ability.query.filter(Ability.name == ability).one_or_none().name
    team_pokemon.ability_desc = Ability.query.filter(Ability.name == ability).one_or_none().desc
    team_pokemon.held_item = Held_item.query.filter(Held_item.name == held_item).one_or_none().id

    db.session.commit()

    return redirect(f"/teams/edit/{team_id}")

@app.route("/teams/save/<int:team_id>/", methods=["POST"])
def add_new_pokemon_to_team(team_id, pokemon_id):
    pokemon_name = request.form.get("pokemon")
    move_1 = request.form.get("move_1")
    move_2 = request.form.get("move_2")
    move_3 = request.form.get("move_3")
    move_4 = request.form.get("move_4")
    held_item = request.form.get("held_item")
    ability = request.form.get("ability")

    #id of the team pokemon to edit.
    team_pokemon_id = request.form.get("team_pokemon_id")

    team_pokemon = Team_pokemon(
        pokemon_id = Pokemon.query.filter(Pokemon.name == pokemon_name).one_or_none().id,
        move_1 = Move.query.filter(Move.name == move_1).one_or_none().id,
        move_2 = Move.query.filter(Move.name == move_2).one_or_none().id,
        move_3 = Move.query.filter(Move.name == move_3).one_or_none().id,
        move_4 = Move.query.filter(Move.name == move_4).one_or_none().id,
        ability = Ability.query.filter(Ability.name == ability).one_or_none().name,
        ability_desc = Ability.query.filter(Ability.name == ability).one_or_none().desc,
        held_item = Held_item.query.filter(Held_item.name == held_item).one_or_none().id
    )

    db.session.add(team_pokemon)
    db.session.commit()

    return redirect(f"/teams/edit/{team_id}")

@app.route("/user/<int:user_id>")
def user_profile(user_id):
    """Show the user's profile."""
    print("user id", user_id)

    user = User.query.get_or_404(user_id)

    return render_template('profile.html', user=user)

@app.route("/pokemon")
def display_pokemon_with_id():
    """Display the data for a Pokemon"""

    pokemon_query =request.args.get("q")

    pokemon = Pokemon.query.filter(Pokemon.name == pokemon_query).one_or_none()

    return render_template("pokemon.html", pokemon=pokemon)

@app.route("/pokemon/<string:pokemon_name>")
def display_pokemon_with_name(pokemon_name):
    """Display the data for a Pokemon"""

    print("pokemon_name", pokemon_name)

    pokemon = Pokemon.query.filter(Pokemon.name == pokemon_name).one_or_none()

    return render_template("pokemon.html", pokemon = pokemon)

@app.route("/teams/initialize", methods=["POST"])
def initialize_team():
    '''Initialize a team object in the sql database with empty data for ease of querying later'''
    team_name = request.form["team_name"]

    if(g.user):
        pokemon1 = Team_pokemon()
        pokemon2 = Team_pokemon()
        pokemon3 = Team_pokemon()
        pokemon4 = Team_pokemon()
        pokemon5 = Team_pokemon()
        pokemon6 = Team_pokemon()

        db.session.add_all([pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6])
        db.session.commit()

        team = Team(
            name = team_name,
            user_id = g.user.id,
            team_pokemon_1 = pokemon1.id,
            team_pokemon_2 = pokemon2.id,
            team_pokemon_3 = pokemon3.id,
            team_pokemon_4 = pokemon4.id,
            team_pokemon_5 = pokemon5.id,
            team_pokemon_6 = pokemon6.id
        )
        db.session.add(team)
        db.session.commit()

        return redirect(f"/teams/create/{team.id}")

    else:
        anon_user = User.query.filter(User.username == "anonymous").one_or_none()
        team = Team(
            name = team_name,
            user_id = anon_user.id
        )
        db.session.add(team)
        db.session.commit()

        team_obj = Team.query.filter(Team.name == team_name).one_or_none()

        return redirect(f"/teams/create/{team_obj.id}")

@app.route("/teams/create/<int:team_id>")
def create_team(team_id):
    """Route to create a new team """

    team = Team.query.get_or_404(team_id)

    return render_template("team_create.html", team = team)

@app.route("/teams/delete/<int:team_id>", methods=["POST"])
def delete_team(team_id):
    '''Route for deleting a team'''

    team = Team.query.get_or_404(team_id)
    if (team.user_id == g.user.id):
        try:
            db.session.delete(team)
            db.session.commit()
            flash("Team deleted successfully")
            return redirect("/")
        except:
            flash("Something went wrong")
            return redirect(f"/teams/{team_id}")
    else:
        flash("Invalid user")
        return redirect(f"/teams/{team_id}")

@app.route("/pokemon/favorite/<int:pokemon_id>", methods=["POST"])
def add_remove_favorite_pokemon(pokemon_id):
    '''Route to add a favorite to a user's profile'''

    curr_pokemon = Pokemon.query.filter(Pokemon.id == pokemon_id).one_or_none()

    if curr_pokemon in g.user.favorites:
        print("removing favorite")
        favorite = Favorite.query.filter(Favorite.user_id == g.user.id).filter(Favorite.pokemon_id == curr_pokemon.id).one_or_none()
        db.session.delete(favorite)
        db.session.commit()
    else:
        print("adding favorite")
        new_favorite = Favorite(
            user_id = g.user.id,
            pokemon_id = pokemon_id,
            shiny = False
        )
        db.session.add(new_favorite)
        db.session.commit()

    return render_template("pokemon.html", pokemon = curr_pokemon)

@app.route("/pokemon/favorite/<int:pokemon_id>/shiny", methods=["POST"])
def add_remove_favorite_pokemon_shiny(pokemon_id):
    '''Route to add a favorite to a user's profile that is specifically going to have the shiny image'''

    curr_pokemon = Pokemon.query.filter(Pokemon.id == pokemon_id).one_or_none()

    if curr_pokemon in g.user.favorites:
        print("removing favorite")
        favorite = Favorite.query.filter(Favorite.user_id == g.user.id).filter(Favorite.pokemon_id == curr_pokemon.id).one_or_none()
        db.session.delete(favorite)
        db.session.commit()
    else:
        print("adding favorite")
        new_favorite = Favorite(
            user_id = g.user.id,
            pokemon_id = pokemon_id,
            shiny = True
        )
        db.session.add(new_favorite)
        db.session.commit()

    return render_template("pokemon.html", pokemon = curr_pokemon)


# routes to return pokemon types directly to frontend
@app.route("/static/images/types/dark.png")
def return_dark_pic():
    return send_file("./static/images/types/Dark.png", attachment_filename='dark.png')

@app.route("/static/images/types/bug.png")
def return_bug_pic():
    return send_file("./static/images/types/Bug.png", attachment_filename='bug.png')

@app.route("/static/images/types/dragon.png")
def return_dragon_pic():
    return send_file("./static/images/types/Dragon.png", attachment_filename='dragon.png')

@app.route("/static/images/types/electric.png")
def return_electric_pic():
    return send_file("./static/images/types/Electric.png", attachment_filename='electric.png')

@app.route("/static/images/types/fairy.png")
def return_fairy_pic():
    return send_file("./static/images/types/Fairy.png", attachment_filename='fairy.png')

@app.route("/static/images/types/fighting.png")
def return_fighting_pic():
    return send_file("./static/images/types/Fighting.png", attachment_filename='fighting.png')

@app.route("/static/images/types/fire.png")
def return_fire_pic():
    return send_file("./static/images/types/Fire.png", attachment_filename='fire.png')

@app.route("/static/images/types/flying.png")
def return_flying_pic():
    return send_file("./static/images/types/Flying.png", attachment_filename='flying.png')

@app.route("/static/images/types/ghost.png")
def return_ghost_pic():
    return send_file("./static/images/types/Ghost.png", attachment_filename='ghost.png')

@app.route("/static/images/types/grass.png")
def return_grass_pic():
    return send_file("./static/images/types/Grass.png", attachment_filename='grass.png')

@app.route("/static/images/types/ground.png")
def return_ground_pic():
    return send_file("./static/images/types/Ground.png", attachment_filename='ground.png')

@app.route("/static/images/types/ice.png")
def return_ice_pic():
    return send_file("./static/images/types/Ice.png", attachment_filename='ice.png')

@app.route("/static/images/types/normal.png")
def return_normal_pic():
    return send_file("./static/images/types/Normal.png", attachment_filename='normal.png')

@app.route("/static/images/types/poison.png")
def return_poison_pic():
    return send_file("./static/images/types/Poison.png", attachment_filename='poison.png')

@app.route("/static/images/types/psychic.png")
def return_psychic_pic():
    return send_file("./static/images/types/Psychic.png", attachment_filename='psychic.png')

@app.route("/static/images/types/rock.png")
def return_rock_pic():
    return send_file("./static/images/types/Rock.png", attachment_filename='rock.png')

@app.route("/static/images/types/steel.png")
def return_steel_pic():
    return send_file("./static/images/types/Steel.png", attachment_filename='steel.png')

@app.route("/static/images/types/water.png")
def return_water_pic():
    return send_file("./static/images/types/Water.png", attachment_filename='water.png')








