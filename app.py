import os

from flask import Flask, render_template, request, flash, redirect, session, g
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
# db.create_all()

@app.route('/')
def homepage():

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

@app.route('/teams')
def display_teams():

    teams = Team.query.all()

    return render_template("/teams.html", teams = teams)

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
    team = Team.query.get_or_404(team_id)

    pokemon = [team.pokemon1, team.pokemon2, team.pokemon3, team.pokemon4, team.pokemon5, team.pokemon6]
    team_pokemon = pokemon[team_slot - 1]

    all_pokemon = [pokemon.asDict() for pokemon in Pokemon.query.all()]
    all_items = [item.name for item in Held_item.query.all()]

    return render_template("team_edit.html", team = team, allPokemon = allPokemon, allItems= allItems, ids = teamPokemonIds)

# @app.route("/teams/save/<int:team_id>/<string:pokemon_name>/<string:move_1>/<string:move_2>/<string:move_3>/<string:move_4>/<string:held_item>", methods=["POST"])
@app.route("/teams/save/<int:team_id>", methods=["POST"])
def save_team_state(team_id):
    pokemon_name = request.form.get("pokemon")
    move_1 = request.form.get("move_1")
    move_2 = request.form.get("move_2")
    move_3 = request.form.get("move_3")
    move_4 = request.form.get("move_4")
    held_item = request.form.get("held_item")
    ability = request.form.get("ability").split(',')

    #id of the team pokemon to edit.
    team_pokemon_id = request.form.get("team_pokemon_id")

    print("pokemon name", pokemon_name)
    print("move 1", move_1)
    print("move2", move_2)
    print("move3", move_3)
    print("MOve4", move_4)
    print("Held_item", held_item)
    print("teampokemodn id", team_pokemon_id)
    print(ability)

    team_pokemon = Team_pokemon.query.get_or_404(team_pokemon_id)

    team_pokemon.pokemon_id = Pokemon.query.filter(Pokemon.name == pokemon_name).one_or_none().id
    team_pokemon.move_1 = Move.query.filter(Move.name == move_1).one_or_none().id
    team_pokemon.move_2 = Move.query.filter(Move.name == move_2).one_or_none().id
    team_pokemon.move_3 = Move.query.filter(Move.name == move_3).one_or_none().id
    team_pokemon.move_4 = Move.query.filter(Move.name == move_4).one_or_none().id
    team_pokemon.ability = ability[0]
    team_pokemon.ability_desc = ability[1]
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

    print("pokemon name", pokemon_name)
    print("move 1", move_1, Move.query.filter(Move.name == move_1).one_or_none())
    print("move 2", move_2)
    print("move 3", move_3)
    print("move 4", move_4)
    print("Held_item", held_item)
    print("team pokemon id", pokemon_id)
    print(ability)

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

@app.route("/pokemon/<int:pokemon_id>")
def display_pokemon_with_id(pokemon_id):
    """Display the data for a Pokemon"""

    print("pokemon_id", pokemon_id)

    pokemon = Pokemon.query.get_or_404(pokemon_id)

    return render_template("pokemon.html", pokemon=pokemon)

@app.route("/pokemon/<string:pokemon_name>")
def display_pokemon_with_name(pokemon_name):
    """Display the data for a Pokemon"""

    print("pokemon_name", pokemon_name)

    pokemon = Pokemon.query.filter(Pokemon.name == pokemon_name).one_or_none()

    return render_template("pokemon.html", pokemon = pokemon)




