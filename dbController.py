import json
from db import SessionLocal, init_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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

def hashPassword(password: str):
    '''
    Helper Function for hashing password. 
    password - String of the password to be hashed
    returns - string of hashed password
    '''
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  
    
def createUser(firstName: str, lastName: str, email: str, username: str, password: str , session: Session):
    '''
    Adds a new user to the User table\n
    firstName: str\n
    lastName: str\n
    email:str\n
    username:str\n
    password:str\n
    session: Session\n
    '''
    passwordHash = hashPassword(password)
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
        