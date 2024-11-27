from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import bcrypt

# Define the base for models
Base = declarative_base()

# Define your models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=func.now())
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(name='{self.first_name}' {self.last_name}, email='{self.email}, username='{self.username}'')>"
    
    def hash_password(password: str):
        '''
        Helper Function for hashing password. 
        password - String of the password to be hashed
        returns - string of hashed password
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
    __tablename__="projects"

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=func.now())
    name = Column(String, nullable=False)
    description = Column(String)
    budgets = relationship("Budget", back_populates="project", cascade="all, delete-orphan")
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="projects")

    def __repr__(self):
        return f"<Project(name='{self.name}', description='{self.description}, budgets'{self.budgets}')>"
    
    
class Budget(Base):
    __tablename__="budgets"

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=func.now())
    budget_code = Column(String, nullable=False)
    usage_description = Column(String) 
    project_id = Column(Integer, ForeignKey('projects.id'))  
    project = relationship("Project", back_populates="budgets")