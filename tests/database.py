# Legacy code!!!!!!!!!!

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app .config import settings
from app.database import get_db
from app.database import Base
from alembic import command

###############
# Creating a test database to not interfer with the dev database

#I created a new fastapi_test database
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




#This lines will override all the get_db() calls of our code, by swapping it with override_get_db()!


@pytest.fixture()
def session():
    #Creates all of our tables
    Base.metadata.drop_all(bind=engine)
    #Dropping tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#pytest -v -s --disable-warnings tests\test_users.py
# note that the script won't work by itself

# New client
@pytest.fixture() # The change of scopre ensures the database does not get delete each time the functions gets called! when setup to module
def client(session): # We call the session for each client!
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# Initial client
'''
@pytest.fixture
def client(session):
    # run our code before we return our test
    # Dropping all the tables
    Base.metadata.drop_all(bind=engine)
    # Creating all the tables
    Base.metadata.create_all(bind=engine)
    # command.upgrade('head') # Alembic equivalent to SQLAlchemy
    yield TestClient(app)
    # run our code after our test finished
    # Initially, we dropped the tables at the end
    # command.downgrade() # Alembic equivalent to SQLAlchemy
''' 