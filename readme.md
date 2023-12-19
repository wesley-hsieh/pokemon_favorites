# Yet Another Pokémon Teambuilder

## Description

A rendition and personal project on the classic Pokémon Teambuilder built and based on a combination of Flask, Jinja, 
PostgreSQL, HTML, CSS, and Javascript. A place for people to generally draft which Pokémon they want to bring, their movesets, abilities, and items as
well as view other people's teams and what they chose to bring in their journey!

## Getting Started

If you wish to simply view the project in action, head over to [yetanotherpokemonteambuilder](https://yetanotherpokemonteambuilder-32a0fcc5ffd6.herokuapp.com/)

### General user flow

Go ahead and register with the site, email is required but no emails will be sent to you so do not worry about that. 
Navigate to your profile and you will see an area that you can create a new team based on whichever name you submit. Once you have decided on the name of your team and submit, 
you'll be redirected to your team creation page. Click on the question mark images to edit that specific slot, in which you will have the option(s) to choose which Pokémon, 
and the rest of the drop downs will be populated afterwards. Make sure to click save and you'll be further redirected back to your team creation page. 

Furthermore, you can look up Pokémon and their base stats, types, and stats in the search bar in the top right by your profile link. Simply input a Pokémon's name you wish to look up.
In the specific Pokémon's page, you'll see a little button by which you can toggle whether or not you wish to see shiny sprite. 

### Dependencies

* This was primarily drafted and ran on an Ubuntu Linux virtual machine, specifically Ubuntu 20.04 LTS.
* The dependencies are as follows
```
Flask-Bcrypt==0.7.1
Flask-DebugToolbar==0.10.1
Flask-SQLAlchemy==2.3.2
Flask-WTF==0.14.2
SQLAlchemy==1.2.12
WTForms==2.2.1
bcrypt==3.1.4
cffi==1.14.2
chardet==3.0.4
click==8.0
cryptography==2.8
gunicorn==20.0.4
idna==2.8
itsdangerous==2.0
requests==2.22.0
urllib3
Flask==1.0.2
Werkzeug==0.14.1
Jinja2==2.10
MarkupSafe==1.1.1
psycopg2-binary==2.8.4
```

### Installing

* The basic requirements to running this is having an ubuntu installation, a postgresql database, python installed on your machine,
preferably python3 and above with ipython installed as well. The specific version that heroku is running this with is python-3.9.18.

* Install a postgresql server and initialize the empty database. I used `sudo apt install postgresql` followed by `sudo service postgresql start` to check if 
the database is running. Once the psql server is confirmed to be online, enter the psql shell via `psql` and simply create the database
via `CREATE DATABASE pokemon_favorites;`. The flask sqlalchemy ORM will take care of all the tables and relations.

* Clone the repository with your desired method, the one I suggest is `git clone git@github.com:wesley-hsieh/pokemon_favorites.git`.

* Once cloned, navigate to the folder, initiate ipython and once the shell is open execute `%run seed.py`. This will populate your database
with data from https://pokeapi.co/ to minimize queries to the api later. 

* Exit the ipython shell and install the project dependencies: `pip install -r requirements.txt`, if you do not have pip installed by default through
your python installation, reference the [docs](https://pip.pypa.io/en/stable/installation/).

### Executing program

* With your dependencies installed, you should be able to simply execute the flask app via `flask run` 
* Navigate to your localhost at port 5000 or `localhost:5000` or `127.0.0.1:5000` and have fun! 

## Acknowledgments

Websites that I took inspiration from
* https://play.pokemonshowdown.com/teambuilder
* https://mypokemonteam.com/

API that I sourced my data from 
* https://pokeapi.co/ 
