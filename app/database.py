from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



'''while True:
    # Try/except: to make sure the internet conection is not an issue
    try:
        host = 'localhost'
        database = 'fastapi'
        my_user = 'postgres'
        password = 'Suckmyd2ck!69'
        conn = psycopg2.connect(host = host, 
                                database = database, 
                                user = my_user, 
                                password = password,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was sucessful!')
        break
    except Exception as error:
        print('Connecting to database failed')
        print('The error was:', error)
        time.sleep(2)'''