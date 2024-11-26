import json
from db import SessionLocal, init_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound, MultipleResultsFound
from model import User
import bcrypt


def startConnection():
    '''
    Initializes database if one does not already exist and returns a session object.
    '''
    # Initialize the database (create tables)
    init_db()
    # Create a database session
    return SessionLocal()

def login(username: str, password: str, session: Session):
    '''
    Queries the database to verify user credentials
    '''
    try:
        user = session.query(User).filter_by(username=username).one()
        is_password = user.check_password(password)
        if is_password:
            return user
        else:
            return False
    except NoResultFound as e:
        raise e
    except MultipleResultsFound as e:
        raise e
    
def create_user(firstName: str, lastName: str, email: str, username: str, password: str , session: Session):
    '''
    Adds a new user to the User table\n
    firstName: str\n
    lastName: str\n
    email:str\n
    username:str\n
    password:str\n
    session: Session\n
    '''
    passwordHash = User.hash_password(password)
    try:
        new_user = User(first_name=firstName, last_name=lastName, email=email, username=username, password=passwordHash)
        session.add(new_user)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise IntegrityError
    except Exception as e:
        session.rollback()
        raise e
        