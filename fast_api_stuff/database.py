from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv

load_dotenv()
environment = getenv("ENVIRONMENT", "local")

if environment == "docker":
    DATABASE_URL = getenv("DATABASE_URL_DOCKER")
else:
    DATABASE_URL = getenv("DATABASE_URL_LOCAL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()