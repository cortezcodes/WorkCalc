from sqlalchemy import Boolean, Column, Date, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=func.now())
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    projects = relationship("Project", back_populates='owner', cascade='all, delete')
    events = relationship("Event", back_populates='owner', cascade='all, delete')

    def __repr__(self):
        return f"<User(name='{self.first_name} {self.last_name}', email='{self.email}', username='{self.username}')>"

    @staticmethod
    def hash_password(password: str):
        '''
        Helper Function for hashing password. 
        '''
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def check_password(self, given_password: str):
        '''
        Helper function for validating password credentials
        '''
        return bcrypt.checkpw(given_password.encode('utf-8'), self.password.encode('utf-8'))

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="projects")
    budgets = relationship("Budget", back_populates='project', cascade='all, delete', lazy="joined")

    def __repr__(self):
        return f"<Project(title='{self.title}', description='{self.description}, budgets='{self.budgets}')>"

class Budget(Base):
    __tablename__="budgets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    budget_code = Column(String, nullable=False, unique=True)
    usage_description = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

    project = relationship("Project", back_populates="budgets")

    def __repr__(self):
        return f"<Budget(budget_code='{self.budget_code}', usage='{self.usage_description}')>"
    
class Event(Base):
    __tablename__="events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(String, nullable=False)
    budget_code = Column(String, nullable=False)
    event_description = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    isComplete = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="events")

    def __repr__(self):
        return f"<Event(project='{self.project}', budget_code='{self.budget_code}', event='{self.event_description}', start_time='{self.start_time}', end_time='{self.end_time}')>"