from db import SessionLocal, init_db
from sqlalchemy.orm import Session
from model import User


def startConnection():
    '''
    Initializes database if one does not already exist and returns a session object.
    '''
    # Initialize the database (create tables)
    init_db()
    # Create a database session
    return SessionLocal()

def isUserNameFree(name:str, session: Session):
    '''
    Function for querying workcalc's database and checking if a username already exist.\n
    name - username to be checked for in the database
    session - session to the database to query against
    
    '''
    response = session.query(User).filter(User.username == name).first()
    if not response:
        return True
    else:
        return False