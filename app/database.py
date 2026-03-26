from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(DATABASE_URL,
                       connect_args={"check_same_thread": False})

#Because SQLite normally allows one thread only.
#FastAPI uses multiple threads, so we disable that restriction.

SessionLocal = sessionmaker(
                        autocommit = False,
                        autoflush=False,
                        bind=engine
                        )

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db #give db session 
    finally:
        db.close() #ensure session close 

#creating dependency for fastapi
"""We create a function that:

opens DB session

gives it to API

closes it automatically"""

"""
    engine	- connects to database
    SessionLocal  -	creates DB sessions
    Base  -	parent class for tables
    get_db - dependency for FastAPI routes
"""


