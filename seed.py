from models import db, User, Feedback
from app import app
import sqlalchemy as db2
from sqlalchemy_utils import database_exists, create_database
from app_long_forms import *
engine = db2.create_engine('postgresql:///user-auth')
if not database_exists(engine.url):
    create_database(engine.url, encoding='SQL_ASCII')
with app.app_context():
    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()
    user1 = User(
        username="UserName",
        password="Password",
        email="test@test.com",
        first_name="First",
        last_name="Last"
    )
    try:
        user1 = user1.hash_password()
        db.session.add_all([user1])
        db.session.commit()
        """
        print(str(user1))
        <User username=UserName email=test@test.com first_name=First last_name=
        Last>
        """
        """Nested try here to receive ID after commit"""
        feedback1 = Feedback(
            title=long_text_64,
            content=long_text_3677,
            user=user1.username
        )
        db.session.add_all([feedback1])
        db.session.commit()

        """        
        print(str(user1))
        <User username=UserName email=test@test.com first_name=First last_name=
        Lastfeed_back_count=1>
        
        print(str(feedback1))
        <Feedback id=1 title=[Sed ut lectus risus. Nam quam du] content=[Lorem 
        ipsum dolor sit amet, cons] username=[UserName]>
        """

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
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error committing data: {e}")
