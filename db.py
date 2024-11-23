from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base

# Configure the database URL
DATABASE_URL = "sqlite:///workcalc_database.db"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)

# Function to initialize the database (create tables)
def init_db():
    Base.metadata.create_all(bind=engine)
