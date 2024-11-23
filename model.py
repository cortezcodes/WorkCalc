from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Define the base for models
Base = declarative_base()

# Define your models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=func.now)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"
