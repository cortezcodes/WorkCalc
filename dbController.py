from datetime import datetime, timedelta
from rich import print
from sqlite3 import Error, OperationalError
from typing import List

from sqlalchemy import DateTime
from db import init_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound, MultipleResultsFound
from model import Budget, Event, Project, User

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

def add_project(title: str, description: str, budgets: List[str], user_id: int):
    '''
    Function for adding new projects to the database.
    returns title of project if successful
    '''
    session  = startConnection()
    current_user = session.query(User).filter_by(id=user_id).first()
    project_title = ""
    try:
        new_project = Project(title=title, description=description, owner=current_user)
        session.add(new_project)

        for budget in budgets:
            new_budget = Budget(budget_code=budget.strip(), project=new_project)
            session.add(new_budget)
        
        session.commit()
        project_title = new_project.title
    except IntegrityError as e: 
        session.rollback()
        print(f"[red]Error:[/red] Project already exist.")
    finally:
        session.close()
        return project_title
    
def get_projects(user_id: int):
    '''
    Returns all projects associated with a user. 
    '''
    session = startConnection()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        projects = user.projects
        return projects
    finally:
        session.close()
    
def delete_project(user_id: int, project_id:int):
    session = startConnection()
    try:
        project = session.query(Project).filter(
            Project.user_id == user_id,
            Project.id == project_id).first()
        if project:
            session.delete(project)
            session.commit()
            return True
        else:
            return False
    finally:
        session.close()

def add_event(user_id: int, project: str, budget: str, 
              event_description: str, start_time: DateTime, isComplete: bool, end_time: DateTime | None = None):
    '''
    Creates an event entry in the event database
    '''
    session = startConnection()
    current_user = session.query(User).filter_by(id=user_id).first()
    try:
        new_event = Event(owner=current_user,project=project, budget_code=budget, event_description=event_description,
                          start_time=start_time, end_time=end_time, isComplete=isComplete)
        session.add(new_event)
        session.commit()
        return new_event
    finally:
        session.close()

def get_active_event(user_id:int, target_date: datetime):
    '''
    Retreives the active event for a given day. 
    '''
    start_of_day = target_date.replace(hour=0, minute=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    session = startConnection()
    try:
        event = session.query(Event).filter(
            Event.user_id == user_id,
            Event.start_time >= start_of_day,
            Event.start_time < end_of_day,
            Event.isComplete == False).first()
        return event
    finally:
        session.close()

def finish_active_event(user_id: int, event_id: int):
    '''
    Close out an active event 
    '''
    session = startConnection()
    try:
        event: Event = session.query(Event).filter(
            Event.user_id == user_id,
            Event.id == event_id,
            Event.isComplete == False
        ).first()
        event.end_time = datetime.now().replace(second=0, microsecond=0)
        event.isComplete = True
        session.commit()
    finally:
        session.close()
    

def get_events_on_date(user_id: int, target_date: datetime):
    '''
    Retrieves all events on a given day
    '''
    start_of_day = target_date.replace(hour=0, minute=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    session = startConnection()
    try:
        events = session.query(Event).filter(
            Event.user_id == user_id,
            Event.start_time >= start_of_day,
            Event.start_time < end_of_day).all()
        
        return events
    finally:
        session.close()

def delete_event(user_id:int, event_id: int):
    '''
    Given an event id, delete the event if the user has access
    '''
    session = startConnection()
    try:
        event = session.query(Event).filter(
            Event.user_id == user_id,
            Event.id == event_id).first()
        if event:
            session.delete(event)
            session.commit()
            print("Event deleted successfully")
    except Error as e:
        print(f"Error in delete_event(): {e}")
    finally:
        session.close()