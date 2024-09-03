from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import  get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags = ['Posts'] #Allows for documentations grouping
)


#@router.get('/', response_model = List[schemas.Post])
#@router.get('/') # We had issues with the schemas
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit:int = 10, skip:int = 0, search: Optional[str] ="" ):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # Select all posts of current user
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        
    return posts


#Within Postman, to send data, you do add the POST request URL, then Body>Raw>JSON and create the JSON file you wanna send
# intial, yet old stuff: def create_posts(payLoad: dict = Body(...)): #the ... inside Body() allows the extraction of what is past to the POST request
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)): #the ... inside Body() allows t 
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # conn.commit()
    # new_post = cursor.fetchone()
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post) # equiv to adding REFRESHING *
    return new_post

#@router.get("/{id}", response_model=schemas.PostOut)
@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} was not found')
    
    # if post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 'Not authorized to perform the action')

    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,  db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
        
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} does not existd')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 'Not authorized to perform the action')
    
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}")
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), response_model = schemas.Post, current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} does not existd')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 'Not authorized to perform the action')
    
    
    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    return post_query.first()


