import json
from sqlite3 import OperationalError
from typing import List
from db import init_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound, MultipleResultsFound
from model import Project, User

def startConnection():
    '''
    Initializes database if one does not already exist and returns a session object.
    '''
    # Initialize the database (create tables)
    sessionLocal: Session = init_db()
    # Create a database session
    return sessionLocal()


def login(username: str, password: str):
    '''
    Queries the database to verify user credentials
    '''
    session = startConnection()
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
    finally:
        session.close()
    
def create_user(firstName: str, lastName: str, email: str, username: str, password: str):
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
    session = startConnection()
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
    finally:
        session.close()

def add_project(title: str, description: str, user_id: int):
    '''
    Function for adding new projects to the database.
    '''
    session  = startConnection()
    current_user = session.query(User).filter_by(id=user_id).first()
    # try:
    new_project = Project(title=title, description=description, owner=current_user)
    session.add(new_project)
    session.commit()
    project_title = new_project.title
    # except Exception as e: 
    #     session.rollback()
    #     raise e
    # finally:
    session.close()
    return project_title
        