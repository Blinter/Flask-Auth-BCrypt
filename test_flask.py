from unittest import TestCase

from app import app
from models import db, User, Feedback
from app_long_forms import *
# Additional Testing
# from models import Pet, db, connect_db

app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_user_auth'
app.config['SQLALCHEMY_ECHO'] = False


with app.app_context():
    db.drop_all()
    db.create_all()


class UserTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Clean up any existing User."""
        with app.app_context():
            with app.test_client() as client:
                db.drop_all()
                db.create_all()
                db.session.commit()
                self.client = app.test_client()
                user1 = User(
                    username="UserName",
                    password="Password",
                    email="test@test.com",
                    first_name="First",
                    last_name="Last"
                )
                user1 = user1.hash_password()
                db.session.add_all([user1])
                db.session.commit()
                feedback1 = Feedback(
                    title=long_text_64,
                    content=long_text_3677,
                    user=user1.username
                )
                db.session.add_all([feedback1])
                db.session.commit()
                feedback2 = Feedback(
                    title=long_text_64,
                    content=long_text_3677,
                    user=user1.username
                )
                db.session.add_all([feedback2])
                db.session.commit()

                user2 = User(
                    username="UserName2",
                    password="Password",
                    email="test@test2.com",
                    first_name="First",
                    last_name="Last"
                )
                user2 = user2.hash_password()
                db.session.add_all([user2])
                db.session.commit()
                feedback3 = Feedback(
                    title=long_text_64,
                    content=long_text_3677,
                    user=user2.username
                )
                feedback4 = Feedback(
                    title="AA" + long_text_64,
                    content=long_text_3677 + "AA",
                    user=user2.username
                )
                db.session.add_all([feedback3, feedback4])
                db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            with app.test_client() as client:
                db.session.rollback()
                db.drop_all()
                db.create_all()
                db.session.commit()

    def test_user_add_form(self):
        """Test that user form is shown."""
        with app.app_context():
            with app.test_client() as client:
                resp = client.get("/register")
                html = resp.get_data(as_text=True)
                self.assertIn('User Registration', html)

    def test_login_page(self):
        """Test that login page is shown."""
        with app.app_context():
            with app.test_client() as client:
                resp = client.get("/login")
                html = resp.get_data(as_text=True)
                self.assertIn('User Login', html)

    def test_form_password_data(self):
        """Test password verification is working."""
        with app.app_context():
            with app.test_client() as client:
                self.assertIn('Incorrect Password',
                              client.post("/login", data=dict({
                                  "username": "UserName",
                                  "password": "Password2"
                                }), follow_redirects=True)
                              .get_data(as_text=True))
                self.assertIn('Welcome First Last!',
                              client.post("/login", data=dict({
                                  "username": "UserName",
                                  "password": "Password"
                              }), follow_redirects=True).get_data(as_text=True))

    def test_user_existing_user_error(self):
        """Test username UNIQUE is working."""
        with app.app_context():
            with app.test_client() as client:
                html = client.post("/register", data=dict({
                    "username": "UserName",
                    "password": "PasswordChanged",
                    "email": "test@test.com",
                    "first_name": "First",
                    "last_name": "Last"
                }), follow_redirects=True).get_data(as_text=True)
                self.assertIn('Username already taken!', html)
                self.assertNotIn('Email already taken!', html)

    def test_user_email_user_error(self):
        """Test Email UNIQUE is working."""
        with app.app_context():
            with app.test_client() as client:
                html = client.post("/register", data=dict({
                    "username": "UserNameChanged",
                    "password": "Password",
                    "email": "test@test.com",
                    "first_name": "First",
                    "last_name": "Last"
                }), follow_redirects=True).get_data(as_text=True)
                self.assertNotIn('Username already taken!', html)
                self.assertIn('Email already taken!', html)

    def test_form_data_shown(self):
        """Test update Feedback is working."""
        with app.app_context():
            with app.test_client() as client:
                client.post("/login", data=dict({
                    "username":"UserName",
                    "password":"Password"
                }), follow_redirects=True)
                self.assertIn('pharetra massa dapibus. ',
                              client.get("/feedback/1/update")
                              .get_data(as_text=True))

    def test_form_data_hidden(self):
        """Test feedback data will not show to other users."""
        with app.app_context():
            with app.test_client() as client:
                client.post("/login", data=dict({
                    "username": "UserName",
                    "password": "Password"
                }), follow_redirects=True).get_data(as_text=True)
                self.assertIn('The selected feedback cannot be edited!',
                              client.get("/feedback/3/update")
                              .get_data(as_text=True))

    def test_form_data_post(self):
        """Test feedback data can be updated."""
        with app.app_context():
            with app.test_client() as client:
                client.post("/login", data=dict({
                    "username": "UserName",
                    "password": "Password"
                }), follow_redirects=True).get_data(as_text=True)
                self.assertIn('Feedback 1 updated!',
                              client.post("/feedback/1/update", data=dict({
                                  "title": "UserName",
                                  "content": "Password"
                              }), follow_redirects=True).get_data(as_text=True))
                self.assertIn('Feedback 2 updated!',
                              client.post("/feedback/2/update", data=dict({
                                  "title": "UserName",
                                  "content": "Password"
                              }), follow_redirects=True).get_data(as_text=True))

    def test_404(self):
        """Test feedback data can be updated."""
        with app.app_context():
            with app.test_client() as client:
                self.assertIn('404 Not Found!',
                              client.get("/feedbackasdas",
                                         follow_redirects=True)
                              .get_data(as_text=True))

    def test_401(self):
        """Test feedback data can be updated."""
        with app.app_context():
            with app.test_client() as client:
                self.assertIn('''You don&#39;t have access!''',
                              client.post("/feedback/1/update", data=dict({
                                  "title": "TestTitle",
                                  "content": "TestContent"
                              }), follow_redirects=True).get_data(as_text=True))
