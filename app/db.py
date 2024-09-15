from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os, dotenv

dotenv.load_dotenv()

MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASS = os.environ.get('MYSQL_PASS')
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_DB = os.environ.get('MYSQL_DB')
MYSQL_PORT = os.environ.get('MYSQL_PORT')

DATABASE_URL = os.getenv('DATABASE_URL', f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.chat_history import ChatHistory

def create_all_tables():
    Base.metadata.create_all(bind=engine)
