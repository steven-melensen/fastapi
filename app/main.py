from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import Settings

# models.Base.metadata.create_all(bind=engine) # line replaced with Alembic!

app = FastAPI()

origins = ["*"] #public API = *, otherwise, write a list of domain names

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#If two get methods have the same path, the first one will be executed
#This is a path operation (synonym = route)
@app.get('/') #The decorator makes the API works. The '/' is the path
def root(): 
    '''
    The name of the function does not matter
    Could be a login function to check username/password
    Everytime we make a change, we must restart the server
    '''
    return {'message': 'Welcome to my api!'}
   




