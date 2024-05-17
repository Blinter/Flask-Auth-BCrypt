"""Models for User-Auth."""
import logging
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True,
                         unique=True)

    password = db.Column(db.Text(),
                         nullable=False)

    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)

    created_feedback = db.relationship('Feedback', cascade="all, delete")

    @property
    def fullname(self):
        """property to return full name"""
        return self.first_name + \
            " " + self.last_name

    def __repr__(self):
        """Show info about user."""

        return (f"<User username={self.username} " +
                f"email={self.email} " +
                f"first_name={self.first_name} " +
                f"last_name={self.last_name}" +
                (f"feed_back_count="
                 f"{self.created_feedback}" if
                 self.created_feedback else "") +
                f">")

    def hash_password(self):
        """Hashing password."""
        self.password = bcrypt.generate_password_hash(self.password).decode(
            "utf8")
        return self

    def authenticate(self, password):
        """Validate that password is correct.
        Return True if valid; else return False.
        """
        # Debug
        # print(bcrypt.generate_password_hash(password).decode(
        #    "utf8"))
        # print(str(bcrypt.check_password_hash(self.password, password)))
        if bcrypt.check_password_hash(self.password, password):
            return True
        else:
            logging.warning(f"Authentication failed for user {self.username}.")
            return False


class Feedback(db.Model):
    """Feedback"""

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                     nullable=False)

    """Should have maximum due to storage constraint calculations"""
    content = db.Column(db.TEXT(),
                         nullable=False)

    user = db.Column(db.String(20), db.ForeignKey('users.username'),
                     nullable=False)

    username = db.relationship("User", backref="feedbacks", viewonly=True)

    def __repr__(self):
        """Show info about feedback."""

        return (f"<Feedback id={self.id}" +
                  (f" title=[{(str(self.title)[:32])}]" if
                 self.title else "") +
                  (f" content=[{(str(self.content)[:32])}]" if
                 self.content else "") +
                f" username=[{self.username.username}]>")
