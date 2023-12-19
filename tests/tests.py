import os
import unittest
from flask_testing import TestCase
from app import app, db

class FlaskAppTests(TestCase):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql:///pokemon_tests"

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    def setUp(self):
        db.create_all()
        self.seed_data()

    def seed_data(self):
        from models import db, connect_db, User, Pokemon, Favorite, Team, Team_pokemon, Held_item, Move, Saved_teams, Ability
        user = User.register(username="dummy", pwd="password", email="dummy@example.com")
        pikachu = Pokemon(name="pikachu", health_stat=35,attack_stat=55, defence_stat=40,special_atk_stat=50, special_def_stat=50, speed_stat=90, dex_number=25, type_1="electric")

        db.session.add(user)
        db.session.add(pikachu)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Plan your Pokémon Teams!', response.data.decode('utf-8'))

    def test_login(self):
        response = self.client.post('/login', data=dict(
            username="dummy",
            password="password"
        ), follow_redirects=True)

        self.assertIn(b'Hello, dummy!', response.data)

    def test_signup(self):
        response = self.client.post('/signup', data=dict(
            username='newuser',
            password='newpassword',
            email='newuser@example.com'
        ), follow_redirects=True)
        self.assertIn(b'Profile', response.data)

    def test_pokemon_lookup(self):
        response = self.client.get('/pokemon/pikachu')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'pikachu', response.data)

if __name__ == '__main__':
    unittest.main()