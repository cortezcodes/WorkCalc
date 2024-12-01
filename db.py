import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base
from rich import print
import time

# Configure the database URL
DATABASE_URL = "sqlite:///workcalc.db"


# Function to initialize the database (create tables)
def init_db():
    # Create the engine
    engine = create_engine(DATABASE_URL)
    if not os.path.exists("workcalc.db"):
        Base.metadata.create_all(bind=engine)
        print("[green]Database initialized[/green]")
        time.sleep(1)
    else:
        print("[green]Database already initialized,\nConnecting..../green]")

        time.sleep(1)

    return  sessionmaker(bind=engine)

