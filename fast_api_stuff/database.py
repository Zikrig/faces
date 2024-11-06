from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from database import Base
# import models

from dotenv import load_dotenv
from os import getenv

load_dotenv()
environment = getenv("ENVIRONMENT", "local")

if environment == "docker":
    DATABASE_URL = getenv("DATABASE_URL_DOCKER")
else:
    DATABASE_URL = getenv("DATABASE_URL_LOCAL")

# print(environment)
# print(DATABASE_URL)


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345@localhost/postgres"
# DATABASE_URL = getenv('DATABASE_URL')
# print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# создаем класс сессии
# SessionLocal = sessionmaker(autoflush=True, bind=engine)
# with engine.connect() as connection:
#     connection.execute(text("ALTER TABLE images ADD COLUMN name VARCHAR NOT NULL;"))

Base = declarative_base()

# Base.metadata.drop_all(engine)

# Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()